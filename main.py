"""项目入口模块"""
import config
from qihoo_360 import Qihoo360User, Qihoo360

from utils import is_in_hour_minute_period


def _check_speedlimit(qihoo: Qihoo360, speedlimit_list):
    """限速业务逻辑"""

    for device in speedlimit_list:
        mac = device.mac
        unlimit_periods = device.unlimit_period

        if is_in_hour_minute_period(*unlimit_periods):
            print(f'设备：{device.name}({mac}) 在不限速时间段内，取消限速')
            qihoo.cancel_speed_limit(mac=mac)

        else:
            limit_speed = device.limit_speed
            print(f'设备：{device.name}({mac}) 限速到 {limit_speed} Kb')
            qihoo.set_speed_limit(mac=mac, upload=limit_speed, download=limit_speed)


def _check_blacklist(qihoo: Qihoo360, blacklist):
    """黑名单业务逻辑"""
    for device in blacklist:
        mac = device.mac
        name = device.name
        unblacklist_period = device.unblacklist_period

        if is_in_hour_minute_period(*unblacklist_period):
            print(f'设备：{name}({mac}) 在白名单时间段内，移除黑名单')
            qihoo.cancel_blacklist(mac=mac)

        else:
            print(f'设备：{name}({mac}) 加入黑名单')
            qihoo.set_blacklist(mac=mac)


def main():
    """主入口"""
    user = Qihoo360User(username=config.USER.username,
                        password=config.USER.password)
    qihoo = Qihoo360(user=user)

    # 需要限速的业务
    _check_speedlimit(qihoo, config.SPEEDLIMIT_LIST)

    # 需要加黑名单的业务
    _check_blacklist(qihoo, config.BLACKLISTS)


main()
