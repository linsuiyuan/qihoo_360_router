"""360限制设备速度模块"""

import requests

from qihoo_client_protocol import QihooClientProtocol


class Qihoo360SpeedlimitMixin(QihooClientProtocol):
    """
    360路由限制设备网络速度 Mixin类
    (貌似没有连接的也可以设置，路由有保存，但限速的设置看不到)
    """

    def _set_speed_limit(self, enable, mac, upload, download):
        data = {
            'enable': f'{enable}',
            'mac': mac,
            'upload': f'{upload}',
            'download': f'{download}',
        }

        response = requests.post('http://192.168.123.1/app/devices/webs/setspeedlimit.cgi',
                                 cookies=self.cookies, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()

    def set_speed_limit(self, mac, upload, download):
        """设置设备限速"""
        return self._set_speed_limit(enable=1, mac=mac, upload=upload, download=download)

    def cancel_speed_limit(self, mac):
        """取消限速"""
        return self._set_speed_limit(enable=0, mac=mac, upload=0, download=0)
