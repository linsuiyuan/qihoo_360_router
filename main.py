"""项目入口模块"""

from config import USER, SPEEDLIMIT_LIST, BLACKLISTS
from qihoo import Qihoo

from qihoo.utils import is_in_time_period


def _check_speedlimit(qihoo: Qihoo, device):
    """限速业务逻辑"""

    mac = device.mac
    unlimit_periods = device.unlimit_period

    if is_in_time_period(*unlimit_periods):
        print(f'设备：{device.name}({mac}) 在不限速时间段内，放宽网速')
        qihoo.speedlimit.set(mac=mac, upload=10 * 1000, download=80 * 1000)

    else:
        limit_speed = device.limit_speed
        print(f'设备：{device.name}({mac}) 限速到 {limit_speed} Kb')
        qihoo.speedlimit.set(mac=mac, upload=limit_speed, download=limit_speed)


def _check_blacklist(qihoo: Qihoo, device):
    """黑名单业务逻辑"""

    mac = device.mac
    name = device.name
    unblacklist_period = device.unblacklist_period

    if is_in_time_period(*unblacklist_period):
        print(f'设备：{name}({mac}) 在白名单时间段内，移除黑名单')
        qihoo.blacklist.remove(mac=mac)

    else:
        print(f'设备：{name}({mac}) 加入黑名单')
        qihoo.blacklist.add(mac=mac)


def check_task(qihoo):

    for device in SPEEDLIMIT_LIST:
        _check_speedlimit(qihoo, device)
    for device in BLACKLISTS:
        _check_blacklist(qihoo, device)


qh = Qihoo(USER.username, USER.password)
check_task(qh)
# 如果有子路由，则同样运行一遍，好像有缓存
mesh_nodes = qh.devices.mesh_node_list()
for node in mesh_nodes:
    url = f"http://{node['br-ip']}"
    print(f"有子路由：{url}，在子路由上执行一遍")
    qh = Qihoo(USER.username, USER.password, router_url=url)
    check_task(qh)
