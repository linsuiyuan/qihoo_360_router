"""
Mixin 类
"""
import warnings

import requests

from protocols import QihooClientProtocol
from utils import qihoo_password_encrypt


class Qihoo360LoginMixin(QihooClientProtocol):
    """360路由登录Mixin类"""

    def get_rank_key(self):
        """获取 rank_key, 登录加密密码需要用到"""
        response = requests.post('http://192.168.123.1/router/get_rand_key.cgi',
                                 headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return {
            'rand_key': data['rand_key'][32:],
            'key_index': data['rand_key'][:32]
        }

    def login(self, username, password):
        """登录请求"""

        key_obj = self.get_rank_key()
        pass_ = qihoo_password_encrypt(key_obj=key_obj, password=password)

        data = {
            'user': username,
            'pass': pass_,
            'form': '1',
        }

        response = requests.post('http://192.168.123.1/router/web_login.cgi',
                                 headers=self.headers,
                                 data=data)
        response.raise_for_status()

        cookies = {
            'Qihoo_360_login': response.cookies.get('Qihoo_360_login'),
            'updateLock': '1',
            'Token-ID': response.json()['Token-ID'],
        }

        return cookies


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


class Qihoo360DevicesMixin(Qihoo360BlacklistMixin, Qihoo360SpeedlimitMixin):
    """360路由设备管理Mixin类，黑名单管理，限速管理等"""

    def mesh_get_topology_info(self):
        """获取链接设备列表信息"""

        response = requests.get('http://192.168.123.1/router/mesh_get_topology_info.cgi',
                                cookies=self.cookies,
                                headers=self.headers)
        response.raise_for_status()

        route_node = response.json()['data'][0]
        # 如果拓扑节点有链接设备，则拼在同一个列表里
        if route_node['mesh_node']:
            mesh_node = route_node['mesh_node'][0]
            if mesh_node['client_node']:
                route_node['client_node'].extend(mesh_node['client_node'])

        return route_node
