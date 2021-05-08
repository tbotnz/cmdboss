import logging
import json
import re
from typing import Any
from concurrent.futures import ThreadPoolExecutor

from pymongo import MongoClient, database

from bson.json_util import dumps, loads
from bson.objectid import ObjectId

from backend.conf.confload import config
from backend.models.system import ResponseBasic
from backend.util.webhook_runner import exec_hook_func

import time

log = logging.getLogger(__name__)


class CMDBOSS_db:

    def __init__(self):
        self.server = config.mongo_server_ip
        self.port = config.mongo_server_port
        self.username = config.mongo_user
        self.password = config.mongo_password

        if self.username:
            self.raw_connection = MongoClient(
                                            host=self.server,
                                            port=self.port,
                                            username=self.username,
                                            password=self.password,
                                            )
        else:
            self.raw_connection = MongoClient(
                                            host=self.server,
                                            port=self.port,
                                            )

        self.base_connection = self.raw_connection.cmdboss

    def run_hooks(self, operation: str, model: str, data: Any):
        filter = {
                    "events.model": model,
                    "events.operation": operation
                }
        hooks = self.query(
            payload=filter,
            model="hooks"
            )

        if len(hooks["result"]) >= 1:
            with ThreadPoolExecutor(config.num_thread_workers) as worker_pool:
                executions = []
                for hook in hooks["result"]:
                    if len(hook["events"]) >= 1:
                        for event in hook["events"]:
                            if event["operation"] == operation:
                                log.info(f"run_hooks: Webhook Executing on {operation} model {model}")
                                send_payload = {
                                    "base64_payload": hook["base64_payload"],
                                    "payload": data
                                }
                                execution = worker_pool.submit(exec_hook_func, send_payload)
                                executions.append(execution)

    def get_model_name(self, path):
        path_array = path.split("/")
        url_parser = {
            r"\/table/.*/": -2,
            r"\/hooks/.*": -2,
            r"\/hooks": -1,
            r"\/models/.*": -2,
        }
        for key in url_parser:
            if re.search(key, path):
                return path_array[url_parser[key]]
        return path_array[-1]

    def ingress_parse_object_id(self, data: dict):
        if data.get("object_id", False):
            data["_id"] = ObjectId(data["object_id"])
            del data["object_id"]
        return data

    def egress_parse_object_id(self, data: list):
        if len(data) >= 1:
            for idx, obj in enumerate(data, start=0):
                obj_id = obj["_id"]["$oid"]
                data[idx]["object_id"] = obj_id
                del data[idx]["_id"]
            return data

    def insert_one(self, model, payload: dict):
        ret = self.base_connection[model].insert_one(payload)
        result = ResponseBasic(status="success", result=[{"object_id": f"{ret.inserted_id}"}]).dict()
        return result

    def insert_many(self, model, payload: list):
        ret = self.base_connection[model].insert_many(payload)
        resp_arr = []
        for obj in ret.inserted_ids:
            resp_arr.append({"object_id": f"{obj}"})
        result = ResponseBasic(status="success", result=resp_arr).dict()
        return result

    def insert(self, model_instance_data: Any, path: str):
        """ wrapper for both insert_one and insert_many"""
        model_name = self.get_model_name(path)
        if isinstance(model_instance_data, list):
            req_data = []
            for item in model_instance_data:
                req_data.append(item.dict())
            result = self.insert_many(model=model_name, payload=req_data)
        else:
            req_data = model_instance_data.dict()
            result = self.insert_one(model=model_name, payload=req_data)
        self.run_hooks(operation="create", model=model_name, data=result)
        return result

    def query(self, model: str, payload: dict):
        """ wrapper for find with filtering """
        cleaned_data = self.ingress_parse_object_id(payload)
        ret = self.base_connection[model].find(cleaned_data)
        temp_json_result = dumps(ret)
        loaded_result = json.loads(temp_json_result)
        final_result = self.egress_parse_object_id(loaded_result)
        if final_result is None or len(loaded_result) < 1:
            final_result = []
        result = ResponseBasic(status="success", result=final_result).dict()
        return result

    def find(self, model: str):
        ret = self.base_connection[model].find()
        temp_json_result = dumps(ret)
        loaded_result = json.loads(temp_json_result)
        final_result = self.egress_parse_object_id(loaded_result)
        if final_result is None:
            final_result = []
        result = ResponseBasic(status="success", result=final_result).dict()
        return result

    def retrieve(self, query_obj: dict, object_id: str, path: str):
        """ wrapper for both find and query"""
        model_name = self.get_model_name(path)
        if query_obj.get("filter", False):
            result = self.query(model=model_name, payload=query_obj["filter"])
        elif object_id:
            query_obj["filter"] = {}
            query_obj["filter"]["object_id"] = object_id
            result = self.query(model=model_name, payload=query_obj["filter"])
        elif object_id is None:
            result = self.find(model=model_name)
        self.run_hooks(operation="retrieve", model=model_name, data=result)
        return result

    def delete(self, query: dict, object_id: str, path: str):
        final_result = []
        model_name = self.get_model_name(path)
        if query.get("filter", False):
            cleaned_data = self.ingress_parse_object_id(query["filter"])
            ret = self.base_connection[model_name].delete_many(cleaned_data)
            if ret.deleted_count >= 1:
                final_result = [{"deleted_object_count": ret.deleted_count}]
        if object_id:
            query["filter"] = {}
            query["filter"]["object_id"] = object_id
            cleaned_data = self.ingress_parse_object_id(query["filter"])
            ret = self.base_connection[model_name].delete_many(cleaned_data)
            if ret.deleted_count >= 1:
                final_result = [{"deleted_object_count": ret.deleted_count}]
        result = ResponseBasic(status="success", result=final_result).dict()
        self.run_hooks(operation="delete", model=model_name, data=result)
        return result

    def update(self, model_instance_data: dict, object_id: str, path: str):
        final_result = []
        model_name = self.get_model_name(path)
        set_data = model_instance_data.dict()
        new_data = { "$set": set_data }
        query = {}
        query["filter"] = {}
        if object_id:
            query["filter"]["object_id"] = object_id
        cleaned_data = self.ingress_parse_object_id(query["filter"])
        ret = self.base_connection[model_name].update_many(cleaned_data, new_data)
        if ret.modified_count >= 1:
            final_result = [{"updated_object_count": ret.modified_count}]
        result = ResponseBasic(status="success", result=final_result).dict()
        self.run_hooks(operation="update", model=model_name, data=result)
        return result