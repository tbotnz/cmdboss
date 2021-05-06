import json

CONFIG_FILENAME = "/code/config.json"


def load_config_files(config_filename: str = CONFIG_FILENAME):
    try:
        with open(config_filename) as infil:
            return json.load(infil)
    except FileNotFoundError:
        raise FileNotFoundError


data = load_config_files()

bind = data["cmdboss_listen_ip"] + ":" + str(data["cmdboss_listen_port"])
workers = data["gunicorn_workers"]
timeout = 3 * 60
keepalive = 24 * 60 * 60
worker_class = "uvicorn.workers.UvicornWorker"
threads = 45
