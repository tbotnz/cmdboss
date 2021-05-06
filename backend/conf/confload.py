import json
import yaml

import logging
import logging.config

DEFAULT_CONFIG_FILENAME = "config.json"


class Config:
    def __init__(self, config_filename=None):
        if config_filename is None:
            config_filename = DEFAULT_CONFIG_FILENAME

        with open(config_filename) as infil:
            data = json.load(infil)

        self.mongo_server_ip = data["mongo_server_ip"]
        self.mongo_server_port = data["mongo_server_port"]
        self.mongo_user = data["mongo_user"]
        self.mongo_password = data["mongo_password"]
        self.api_key = data["api_key"]
        self.api_key_name = data["api_key_name"]
        self.gunicorn_workers = data["gunicorn_workers"]
        self.listen_ip = data["cmdboss_listen_ip"]
        self.listen_port = data["cmdboss_listen_port"]
        self.cmdboss_http_https = data["cmdboss_http_https"]
        self.model_dir = data["model_dir"]
        self.hook_dir = data["hook_dir"]
        self.log_config_filename = data["log_config_filename"]

    def setup_logging(self, max_debug=False):
        with open(self.log_config_filename) as infil:
            log_config_dict = yaml.load(infil, Loader=yaml_loader)

        if max_debug:
            for handler in log_config_dict["handlers"].values():
                handler["level"] = "DEBUG"

            for logger in log_config_dict["loggers"].values():
                logger["level"] = "DEBUG"

            log_config_dict["root"]["level"] = "DEBUG"

        logging.config.dictConfig(log_config_dict)
        log.info(f"confload: Logging setup @ {__name__}")


config = Config()

log = logging.getLogger(__name__)

try:
    yaml_loader = yaml.CSafeLoader
except AttributeError:
    yaml_loader = yaml.SafeLoader
