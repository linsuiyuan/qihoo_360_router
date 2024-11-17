import warnings

import httpx

from config import ROUTE_URL
from qihoo.utils import qihoo_aes_decrypt, qihoo_aes_encrypt


class Router:
    """路由基类"""
    # 路由器地址
    baseurl: str
    # 路由器全局网络请求实例
    req: httpx.Client


class RouterPlugin:
    """路由插件，实现路由某项功能的类的基类"""

    def __init__(self, router: Router):
        self.baseurl = router.baseurl
        self.req = router.req


class BlackList(RouterPlugin):
    """黑名单类"""

    def list(self):
        """获取黑名单列表"""
        response = self.req.get(f'{self.baseurl}/app/devices/webs/getblacklist.cgi')
        response.raise_for_status()
        return response.json()

    def exists(self, mac):
        """
        判断是否在黑名单中
        :param mac: 设备mac地址
        :return:
        """
        blacklist = self.list()
        blacklist = blacklist['data']
        for device in blacklist:
            if mac.lower() == device['mac'].lower():
                return True
        return False

    def add(self, mac):
        """
        添加黑名单
        :param mac: 设备mac地址
        :return:
        """

        warnings.warn("【注意】添加黑名单后取消黑名单，有时需要重启路由才能生效！")

        response = self.req.post(f'{self.baseurl}/app/devices/webs/setblacklist.cgi',
                                 data={'mac': mac})
        response.raise_for_status()
        return response.json()

    def remove(self, mac):
        """
        移除黑名单
        :param mac: 设备mac地址
        :return:
        """
        response = self.req.post(f'{self.baseurl}/app/devices/webs/cancelblacklist.cgi',
                                 data={'mac': mac})
        response.raise_for_status()
        return response.json()


class SpeedLimit(RouterPlugin):
    """
    360路由限制设备网络速度。
    (貌似没有连接的也可以设置，路由有保存，但限速的设置看不到)
    """

    def _set(self, enable, mac, upload, download):
        data = {
            'enable': f'{enable}',
            'mac': mac,
            'upload': f'{upload}',
            'download': f'{download}',
        }

        response = self.req.post(f'{self.baseurl}/app/devices/webs/setspeedlimit.cgi',
                                 data=data)
        response.raise_for_status()
        return response.json()

    def set(self, mac, upload, download):
        """设置设备限速"""
        return self._set(enable=1, mac=mac, upload=upload, download=download)

    def cancel(self, mac):
        """取消限速"""
        return self._set(enable=0, mac=mac, upload=0, download=0)


class Devices(RouterPlugin):
    """360路由设备管理Mixin类，黑名单管理，限速管理等"""

    def topology_info(self):
        """获取拓扑网络所有设备列表信息"""
        response = self.req.get(f'{self.baseurl}/router/mesh_get_topology_info.cgi')
        response.raise_for_status()

        # client_node 表示设备节点
        # mesh_node 表示拓扑路由节点
        route_node = response.json()['data'][0]

        return route_node

    def list(self):
        """获取连接的设备列表"""
        response = self.req.get(f'{self.baseurl}/app/devices/webs/getdeviceslist.cgi')
        response.raise_for_status()
        data = response.json()['data']
        return data

    def mesh_node_list(self):
        topology_info = self.topology_info()
        mesh_nodes = topology_info["mesh_node"]
        if mesh_nodes:
            for node in mesh_nodes:
                yield node


class VirtualService(RouterPlugin):
    """
    端口映射相关功能
    """

    def list(self):
        """端口映射列表"""
        response = self.req.post(f'{self.baseurl}/app/portmap/webs/virtual_service_list_show.cgi')
        response.raise_for_status()
        return response.json()

    def _add_del(self, name, internal_ip, external_port, internal_port, mode):
        """
        添加或删除端口映射
        :param name: 端口名称
        :param internal_ip: 内部ip
        :param external_port: 外部端口
        :param internal_port: 内部端口
        :param mode: 添加或删除，0表示添加，2表示删除
        """
        data = {
            'name': name,
            'in_ip': internal_ip,
            'protocol': 'tcp',
            'out_start_port': external_port,
            'out_end_port': external_port,
            'in_start_port': internal_port,
            'in_end_port': internal_port,
            'uiname': 'ALL',
            'mode': mode,
        }

        response = self.req.post(f'{self.baseurl}/app/portmap/webs/virtual_service_add_del.cgi',
                                 data=data)
        response.raise_for_status()

        return response.json()

    def add(self, name, internal_ip, external_port, internal_port):
        """
        添加端口映射
        """
        return self._add_del(name=name,
                             internal_ip=internal_ip,
                             external_port=external_port,
                             internal_port=internal_port,
                             mode=0)

    def delete(self, name, internal_ip, external_port, internal_port):
        """
        删除端口映射
        """
        return self._add_del(name=name,
                             internal_ip=internal_ip,
                             external_port=external_port,
                             internal_port=internal_port,
                             mode=2)

    def clean(self):
        """
        清除全部端口映射
        """
        response = self.req.post(f'{self.baseurl}/app/portmap/webs/virtual_service_clean.cgi')
        response.raise_for_status()

        return response.json()


class Qihoo(Router):
    """360路由"""

    def __init__(self, username, password, router_url=ROUTE_URL):
        self.username = username
        self.password = password
        self.baseurl = router_url

        self.req = httpx.Client(headers={'Referer': 'default'})

        self.blacklist = BlackList(self)
        self.speedlimit = SpeedLimit(self)
        self.devices = Devices(self)
        self.virtualservice = VirtualService(self)

        self._login()

    def _get_rank_key(self):
        """获取 rank_key, 登录加密密码需要用到"""

        response = self.req.post(f'{self.baseurl}/router/get_rand_key.cgi')
        response.raise_for_status()
        data = response.json()
        return {
            'rand_key': data['rand_key'][32:],
            'key_index': data['rand_key'][:32]
        }

    def _password_encrypt(self, key_obj, password):
        """360路由密码加密"""
        password = qihoo_aes_decrypt(password[:32], password[32:])
        encrypt_pass = qihoo_aes_encrypt(rand_key_hex=key_obj['rand_key'],
                                         text=password)
        pass_ = key_obj['key_index'] + encrypt_pass
        return pass_

    def _login(self):
        key_obj = self._get_rank_key()
        pwd = self._password_encrypt(key_obj=key_obj, password=self.password)

        data = {
            'user': self.username,
            'pass': pwd,
            'form': '1',
        }

        response = self.req.post(f'{self.baseurl}/router/web_login.cgi',
                                 data=data)
        response.raise_for_status()

        cookies = {
            'Qihoo_360_login': response.cookies.get('Qihoo_360_login'),
            'updateLock': '1',
            'Token-ID': response.json()['Token-ID'],
        }
        self.req.cookies.update(cookies)
