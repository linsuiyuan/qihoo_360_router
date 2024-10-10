"""项目入口模块"""
import asyncio

import config
from qihoo_360 import Qihoo360

from utils import is_in_time_period


async def _check_speedlimit(sem, qihoo: Qihoo360, device):
    """限速业务逻辑"""

    mac = device.mac
    unlimit_periods = device.unlimit_period

    async with sem:
        if is_in_time_period(*unlimit_periods):
            print(f'设备：{device.name}({mac}) 在不限速时间段内，取消限速')
            await qihoo.cancel_speed_limit(mac=mac)

        else:
            limit_speed = device.limit_speed
            print(f'设备：{device.name}({mac}) 限速到 {limit_speed} Kb')
            await qihoo.set_speed_limit(mac=mac, upload=limit_speed, download=limit_speed)


async def _check_blacklist(sem, qihoo: Qihoo360, device):
    """黑名单业务逻辑"""

    mac = device.mac
    name = device.name
    unblacklist_period = device.unblacklist_period

    async with sem:
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
    # 限制同时运行的任务数量
    sem = asyncio.Semaphore(5)
    coros = []
    # 需要限速的业务
    coros.extend([_check_speedlimit(sem, qihoo, device) for device in config.SPEEDLIMIT_LIST])

    # 需要加黑名单的业务
    coros.extend([_check_blacklist(sem, qihoo, device) for device in config.BLACKLISTS])

    await asyncio.gather(*coros)


asyncio.run(main())
