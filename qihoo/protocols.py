"""遵循360路由网络请求的协议"""
from typing import Protocol


class QihooClientProtocol(Protocol):
    """
    遵循360路由网络请求的协议，需包含属性 headers 和 cookies
    """
    @property
    def headers(self) -> dict:
        """headers 属性"""
        raise AttributeError('必须实现 headers 属性')

    @property
    def cookies(self) -> dict:
        """cookies属性"""
        raise AttributeError('必须实现 cookies 属性')
