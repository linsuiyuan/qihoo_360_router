import httpx

from config import ROUTE_URL
from qihoo.utils import qihoo_aes_decrypt, qihoo_aes_encrypt


class Router:
    """路由基类"""
    req: httpx.Client


class Qihoo(Router):
    """360路由"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.req = httpx.Client(headers={'Referer': 'default'})

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
