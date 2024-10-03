"""黑名单模块"""
import warnings

import requests

from qihoo_client_protocol import QihooClientProtocol


class Qihoo360BlacklistMixin(QihooClientProtocol):
    """360路由黑名单 Mixin类"""

    def get_blacklist(self):
        """获取黑名单列表"""

        response = requests.get('http://192.168.123.1/app/devices/webs/getblacklist.cgi',
                                cookies=self.cookies, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def is_in_blacklist(self, mac):
        """
        判断是否在黑名单中
        :param mac: 设备mac地址
        :return:
        """
        blacklist = self.get_blacklist()['data']
        for device in blacklist:
            if mac.lower() == device['mac'].lower():
                return True
        return False

    def set_blacklist(self, mac):
        """
        设置黑名单
        :param mac: 设备mac地址
        :return:
        """

        warnings.warn("【注意】设置黑名单后取消黑名单，有时需要重启路由才能生效！")

        data = {'mac': mac, }
        response = requests.post('http://192.168.123.1/app/devices/webs/setblacklist.cgi',
                                 cookies=self.cookies, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()

    def cancel_blacklist(self, mac):
        """
        取消黑名单
        :param mac: 设备mac地址
        :return:
        """
        data = {'mac': mac, }
        response = requests.post('http://192.168.123.1/app/devices/webs/cancelblacklist.cgi',
                                 cookies=self.cookies, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()
