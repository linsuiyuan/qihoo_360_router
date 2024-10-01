"""360路由登录Mixin"""
from abc import abstractmethod

import requests

from qihoo_client_protocol import QihooClientProtocol
from utils import qihoo_password_encrypt


class Qihoo360LoginMixin(QihooClientProtocol):
    """360路由登录Mixin类"""

    # noinspection PyMethodMayBeStatic
    def get_rank_key(self):
        """获取 rank_key, 登录加密密码需要用到"""
        response = requests.post('http://192.168.123.1/router/get_rand_key.cgi')
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

