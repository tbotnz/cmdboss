import logging

import base64
import os

from typing import Dict

from backend.conf.confload import config

from backend.models.system import ResponseBasic

from backend.util.exceptions import (
    CMDBOSSFileExists
)

log = logging.getLogger(__name__)


class FileMgr:

    def __init__(self):
        self.path_lookup = {
            "model": {"path": config.model_dir, "extn": ".py"},
            "hook": {"path": config.hook_dir, "extn": ".py"}
        }

    def create_file(self, payload: Dict[str, str]):
        raw_base = base64.b64decode(payload["base64_payload"]).decode('utf-8')
        template_path = self.path_lookup[payload["route_type"]]["path"] + payload["name"] + self.path_lookup[payload["route_type"]]["extn"]
        if os.path.exists(template_path):
            raise CMDBOSSFileExists
        with open(template_path, "w") as file:
            file.write(raw_base)
        resultdata = ResponseBasic(status="success", result=[{"created": payload["name"]}]).dict()
        return resultdata

    def delete_file(self, payload: Dict[str, str]):
        template_path = self.path_lookup[payload["route_type"]]["path"] + payload["name"] + self.path_lookup[payload["route_type"]]["extn"]
        os.remove(template_path)
        resultdata = ResponseBasic(status="success", result=[{"deleted": payload["name"]}]).dict()
        return resultdata

    def retrieve_file(self, payload: Dict[str, str]):
        template_path = self.path_lookup[payload["route_type"]]["path"] + payload["name"] + self.path_lookup[payload["route_type"]]["extn"]
        result = None
        with open(template_path, "r") as file:
            result = file.read()
        raw_base = base64.b64encode(result.encode('utf-8'))
        resultdata = ResponseBasic(status="success", result=[{"base64_payload": raw_base}]).dict()
        return resultdata

    def retrieve_files(self, payload: Dict[str, str]):
        path = self.path_lookup[payload["route_type"]]["path"]
        strip_exten = self.path_lookup[payload["route_type"]]["extn"]
        files = []
        fileresult = []
        for r, d, f in os.walk(path):
            for file in f:
                file.strip(path)
                files.append(os.path.join(r, file))
        if len(files) > 0:
            for f in files:
                if "__init__" not in f:
                    if "__pycache__" not in f:
                        if strip_exten:
                            if strip_exten in f:
                                ftmpfile = f.replace(strip_exten, '')
                                fileresult.append(ftmpfile.replace(path, ''))
        resultdata = ResponseBasic(status="success", result=fileresult).dict()
        return resultdata

def func_retrieve_files(payload):
    fmgr = FileMgr()
    return fmgr.retrieve_files(payload)