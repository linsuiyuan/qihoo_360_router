"""360路由模块功能"""
from functools import cached_property

from mixins import Qihoo360LoginMixin
from mixins import Qihoo360DevicesMixin
from models import Qihoo360User


class NotLoggedInError(Exception):
    """未登录异常"""


class Qihoo360(Qihoo360DevicesMixin, Qihoo360LoginMixin):
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
