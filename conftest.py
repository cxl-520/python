from pathlib import Path
import logging.config

import pytest
import requests

from common.conftest import test_login1
from common.conftest import test_login2
from common.conftest import test_login3


def pytest_configure(config):
    """在 pytest 配置阶段设置全局 base_url"""
    config.base_url = "http://idrc.iflight-rc.com/api"
    logs_dir = Path(__file__).resolve().parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    config_path = logs_dir / "logging.ini"
    if config_path.exists():
        logging.config.fileConfig(config_path, disable_existing_loggers=False)

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    """从 pytest 配置中获取 base_url"""
    return pytestconfig.base_url