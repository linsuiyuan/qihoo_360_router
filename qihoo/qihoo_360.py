"""360路由模块功能"""
from functools import cached_property

from qihoo.mixins import LoginMixin
from qihoo.mixins import SettingsMixin
from qihoo.mixins import DevicesMixin


class Qihoo360(SettingsMixin, DevicesMixin, LoginMixin):
    """360路由类"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._cookies = None

    @property
    def headers(self) -> dict:
        """headers 属性"""
        # referer只要有值就行，不检查具体值
        return {'Referer': 'default'}

    @cached_property
    def cookies(self):
        return self.login(username=self.username,
                          password=self.password)
