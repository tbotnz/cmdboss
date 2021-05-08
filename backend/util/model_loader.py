import logging

from backend.cmdboss_db import cmdb_oss

from backend.util.file_mgr import FileMgr


log = logging.getLogger(__name__)


def reload_models():
    q = {}
    fmgr = FileMgr()
    result = cmdb_oss.retrieve(query_obj=q, object_id=None, path=f"/models")
    # determine if reload required
    if len(result["result"]) >= 1:
        models_on_disk = fmgr.retrieve_files({"route_type": "model"})
        if len(models_on_disk["result"]) >= 1:
            for running_model in models_on_disk["result"]:
                del_payload = {
                    "route_type": "model",
                    "name": running_model
                }
                fmgr.delete_file(del_payload)
        log.info(f"{models_on_disk}")
        for model in result["result"]:
            log.info(f'CMDBOSS: Reloading model {model["object_id"]}')
            model_code = {
                "base64_payload": model["base64_payload"],
                "route_type": "model",
                "name": model["name"]
            }
            fmgr.create_file(model_code)
