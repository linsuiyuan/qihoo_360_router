"""360路由模块功能"""
from functools import cached_property

from mixins import LoginMixin
from mixins import SettingsMixin
from mixins import DevicesMixin
from models import Qihoo360User


class Qihoo360(SettingsMixin, DevicesMixin, LoginMixin):
    """360路由类"""

    def __init__(self, user: Qihoo360User):
        self.user = user
        self._cookies = None

    @classmethod
    def create_from(cls, *, username, password) -> "Qihoo360":
        """直接使用用户名、密码创建实例"""
        user = Qihoo360User(username, password)
        return Qihoo360(user)

    @property
    def headers(self) -> dict:
        """headers 属性"""
        # referer只要有值就行，不检查具体值
        return {'Referer': 'default'}

    @cached_property
    def cookies(self):
        return self.login(username=self.user.username,
                          password=self.user.password)
