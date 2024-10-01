"""遵循360路由网络请求的协议"""
from typing import Protocol


class QihooClientProtocol(Protocol):
    """
    遵循360路由网络请求的协议，需包含属性 headers 和 cookies
    """
    @property
    def headers(self) -> dict: ...

    @property
    def cookies(self) -> dict: ...
