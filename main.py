"""项目入口模块"""
import trio

import config
from qihoo_360 import Qihoo360

from utils import is_in_time_period
from utils import run_with_semaphore

# 限制同时运行的任务数量
sem = trio.Semaphore(5)


@run_with_semaphore(sem)
async def _check_speedlimit(qihoo: Qihoo360, device):
    """限速业务逻辑"""

    mac = device.mac
    unlimit_periods = device.unlimit_period

    if is_in_time_period(*unlimit_periods):
        print(f'设备：{device.name}({mac}) 在不限速时间段内，放宽网速')
        await qihoo.set_speed_limit(mac=mac, upload=10 * 1000, download=80 * 1000)

    else:
        limit_speed = device.limit_speed
        print(f'设备：{device.name}({mac}) 限速到 {limit_speed} Kb')
        await qihoo.set_speed_limit(mac=mac, upload=limit_speed, download=limit_speed)


@run_with_semaphore(sem)
async def _check_blacklist(qihoo: Qihoo360, device):
    """黑名单业务逻辑"""

    mac = device.mac
    name = device.name
    unblacklist_period = device.unblacklist_period

    if is_in_time_period(*unblacklist_period):
        print(f'设备：{name}({mac}) 在白名单时间段内，移除黑名单')
        await qihoo.cancel_blacklist(mac=mac)

    else:
        print(f'设备：{name}({mac}) 加入黑名单')
        await qihoo.set_blacklist(mac=mac)


async def main():
    """主入口"""
    qihoo = Qihoo360.create_from(username=config.USER.username,
                                 password=config.USER.password)

    async with trio.open_nursery() as nursery:
        for device in config.SPEEDLIMIT_LIST:
            nursery.start_soon(_check_speedlimit, qihoo, device)
        for device in config.BLACKLISTS:
            nursery.start_soon(_check_blacklist, qihoo, device)


trio.run(main)
# 如果有子路由，则同样运行一遍，好像有缓存
if config.SUB_ROUTE_URL:
    print(f"有子路由：{config.SUB_ROUTE_URL}，在子路由上执行一遍")
    ROUTE_URL = config.ROUTE_URL
    config.ROUTE_URL = config.SUB_ROUTE_URL
    trio.run(main)
    config.ROUTE_URL = ROUTE_URL
