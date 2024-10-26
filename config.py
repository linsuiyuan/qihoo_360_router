"""配置文件"""
import json
import os
from typing import NamedTuple


class UserConfig(NamedTuple):
    """
    用户配置类
    """
    username: str
    password: str


class SpeedlimitDeviceConfig(NamedTuple):
    """
    速度限制设备配置类
    """
    name: str
    mac: str
    unlimit_period: list[str]
    limit_speed: int


class BlacklistDeviceConfig(NamedTuple):
    """
    黑名单设置配置类
    """
    name: str
    mac: str
    unblacklist_period: list[str]


class VirtualServiceConfig(NamedTuple):
    """
    端口映射配置类
    """
    name: str
    internal_ip: str
    internal_port: int
    external_port: int


_qihoo_360 = json.loads(os.getenv('QIHOO_360'))

"""
360路由地址
"""
ROUTE_URL = _qihoo_360['route_url']
SUB_ROUTE_URL = _qihoo_360.get("sub_route_url", None)

"""
360路由用户
"""
_user = _qihoo_360['user']
USER = UserConfig(_user['username'], _user['password'])

"""
限速设备列表
"""
_speedlimits = _qihoo_360['speedlimits']
_device_list: list[dict] = _speedlimits['device_list']
_default_unlimit_period = _speedlimits['default_unlimit_period']
_default_limit_speed = _speedlimits['default_limit_speed']
SPEEDLIMIT_LIST = [SpeedlimitDeviceConfig(
    name=d['name'],
    # 统一转为小写，方便比较
    mac=d['mac'].lower(),
    # 有值取值，没值取默认值
    unlimit_period=d.get('unlimit_period', _default_unlimit_period),
    limit_speed=d.get('limit_speed', _default_limit_speed)
) for d in _device_list]

"""
黑名单列表
"""
_blacklists = _qihoo_360['blacklists']
_device_list: list[dict] = _blacklists['device_list']
_default_unblacklist_period = _blacklists['default_unblacklist_period']
BLACKLISTS = [BlacklistDeviceConfig(
    name=d['name'],
    mac=d['mac'],
    # 有值取值，没值取默认值
    unblacklist_period=d.get('unblacklist_period', _default_unblacklist_period)
) for d in _device_list]


"""
端口映射
"""
_virtual_services = os.getenv("QIHOO_360_VIRTUAL_SERVICES")
_virtual_services = (json.loads(_virtual_services)
                     if _virtual_services
                     else [])
QIHOO_360_VIRTUAL_SERVICES = [VirtualServiceConfig(name, in_ip, in_port, ex_port)
                              for name, in_ip, in_port, ex_port in _virtual_services]

if __name__ == '__main__':
    print(_qihoo_360)
    print(QIHOO_360_VIRTUAL_SERVICES)
