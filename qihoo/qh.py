import warnings

import httpx

from config import ROUTE_URL, USER
from qihoo.utils import qihoo_aes_decrypt, qihoo_aes_encrypt


class Router:
    """路由基类"""
    req: httpx.Client


class BlackList:

    def __init__(self, router: Router):
        self.req = router.req

    def list(self):
        """获取黑名单列表"""
        response = self.req.get(f'{ROUTE_URL}/app/devices/webs/getblacklist.cgi')
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

    def set(self, mac):
        """
        设置黑名单
        :param mac: 设备mac地址
        :return:
        """

        warnings.warn("【注意】设置黑名单后取消黑名单，有时需要重启路由才能生效！")

        response = self.req.post(f'{ROUTE_URL}/app/devices/webs/setblacklist.cgi',
                                 data={'mac': mac})
        response.raise_for_status()
        return response.json()

    def remove(self, mac):
        """
        移除黑名单
        :param mac: 设备mac地址
        :return:
        """
        response = self.req.post(f'{ROUTE_URL}/app/devices/webs/cancelblacklist.cgi',
                                 data={'mac': mac})
        response.raise_for_status()
        return response.json()


class Qihoo(Router):
    """360路由"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.req = httpx.Client(headers={'Referer': 'default'})
        self.blacklist = BlackList(self)

        self._login()

    def _get_rank_key(self):
        """获取 rank_key, 登录加密密码需要用到"""

        response = self.req.post(f'{ROUTE_URL}/router/get_rand_key.cgi')
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

        response = self.req.post(f'{ROUTE_URL}/router/web_login.cgi',
                                 data=data)
        response.raise_for_status()

        cookies = {
            'Qihoo_360_login': response.cookies.get('Qihoo_360_login'),
            'updateLock': '1',
            'Token-ID': response.json()['Token-ID'],
        }
        self.req.cookies.update(cookies)


if __name__ == '__main__':
    qh = Qihoo(USER.username, USER.password)
    print(qh.blacklist.list())
