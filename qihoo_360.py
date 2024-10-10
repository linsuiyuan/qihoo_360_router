"""360路由模块功能"""
from dataclasses import dataclass

from mixins import Qihoo360LoginMixin
from mixins import Qihoo360DevicesMixin


@dataclass
class Qihoo360User:
    """360路由用户类"""
    username: str
    password: str


@dataclass
class Qihoo360Device:
    """360路由连接设备类"""
    # 设备mac地址
    mac: str
    # 设备ip
    ip: str
    # 速度限制标志
    limit_enable: int
    limit_up_speed: int
    limit_down_speed: int
    second: int
    login_time: int
    # 设备名称，一般是英文的
    name: str
    # 设备标签，一般是中文
    device_label: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Qihoo360Device':
        """从字典中创建实例"""
        # 使用字典解包，提供默认值
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})  # noqa


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

    @property
    def cookies(self):
        """cookies属性"""
        if self._cookies is None:
            # 有时效性，所以不用缓存
            self._cookies = self.login(self.user.username, self.user.password)
        return self._cookies

    @property
    def device_list(self):
        """连接设备列表"""
        router_info = self.mesh_get_topology_info()
        nodes = router_info['client_node']
        return [Qihoo360Device.from_dict(n) for n in nodes]
