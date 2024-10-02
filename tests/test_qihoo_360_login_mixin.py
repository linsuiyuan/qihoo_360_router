"""测试 qihoo_360_login_mixin """

from qihoo_360_login_mixin import Qihoo360LoginMixin
import config


class Qihoo360LoginClient(Qihoo360LoginMixin):
    @property
    def headers(self):
        """headers"""
        return {'Referer': 'default'}


def test_get_rank_key():
    mixin = Qihoo360LoginClient()
    result = mixin.get_rank_key()
    print(result)
    assert 'rand_key' in result
    assert 'key_index' in result


def test_login():

    mixin = Qihoo360LoginClient()
    cookies = mixin.login(username=config.USERNAME, password=config.PASSWORD)
    print(cookies)
    assert 'Qihoo_360_login' in cookies
    assert 'Token-ID' in cookies
