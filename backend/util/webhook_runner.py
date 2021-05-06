import importlib
import json
import logging

from typing import Optional

from backend.conf.confload import config

from backend.util.file_mgr import FileMgr

import uuid

log = logging.getLogger(__name__)


class hook_runner(FileMgr):

    def __init__(self, hook_code, hook_payload):
        super().__init__()
        self.hook_raw_name = str(uuid.uuid4())
        self.hook_code = {
            "base64_payload": hook_code,
            "route_type": "hook",
            "name": self.hook_raw_name
        }
        self.hook_dir_path = config.hook_dir
        self.hook_args = hook_payload
        self.hook_name = self.hook_dir_path.replace("/",".") + self.hook_raw_name

    def hook_exec(self):
        try:
            self.create_file(self.hook_code)
            log.info(f"hook_exec: running hook {self.hook_name}")
            module = importlib.import_module(self.hook_name)
            run_whook = getattr(module, "run_hook")
            run_whook(payload=self.hook_args)
            self.delete_file(self.hook_code)
        except Exception as e:
            self.delete_file(self.hook_code)
            log.error(f"hook_exec: hook error {self.hook_name} error {e}")


def exec_hook_func(payload: dict):
    code = payload["base64_payload"]
    payload = payload.get("payload", None)
    hook = hook_runner(hook_code=code, hook_payload=payload)
    hook.hook_exec()
