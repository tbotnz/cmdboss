import logging

from typing import Optional

"""
default hook and boilerplate hook template
IMPORTANT NOTES:
    - hook function name must be "run_hook"
    - payload is a dict containing the record
"""

log = logging.getLogger(__name__)


def run_hook(payload: Optional[dict] = None):
    try:
        # put your code here
        log.info("im a stupid hook")
    except Exception:
        log.error("im a stupid broken hook")