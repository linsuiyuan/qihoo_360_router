"""测试的一些初始化"""

import pytest
from dotenv import load_dotenv


load_dotenv("../dev.env")
import config  # noqa: E402
from qihoo_360 import Qihoo360  # noqa: E402


@pytest.fixture(scope='session')
def router():
    """360路由实例"""
    client = Qihoo360.create_from(username=config.USER.username,
                                  password=config.USER.password)
    yield client
