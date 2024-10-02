"""项目入口模块"""
import config
from qihoo_360 import Qihoo360User, Qihoo360

from utils import is_in_hour_minute_period


def main():
    """主入口"""
    user = Qihoo360User(username=config.USERNAME,
                        password=config.PASSWORD)
    qihoo = Qihoo360(user=user)

    # 需要限速的业务
    speed_limit_obj = {d['mac']: d for d in config.SPEEDLIMIT_LIST}

    for mac, obj in speed_limit_obj.items():

        limit_periods = obj['limit_period']

        if not is_in_hour_minute_period(*limit_periods):
            print(f'设备：{obj["name"]}({mac}) 不在限速时间段内，取消限速')
            qihoo.cancel_speed_limit(mac=mac)

        else:
            limit_speed = obj['limit_speed']
            print(f'设备：{obj["name"]}({mac}) 限速到 {limit_speed} Kb')
            qihoo.set_speed_limit(mac=mac, upload=limit_speed, download=limit_speed)


main()
