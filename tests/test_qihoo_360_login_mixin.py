"""测试 qihoo_360_login_mixin """

from qihoo_360_login_mixin import Qihoo360LoginMixin
import config


def test_get_rank_key(router):
    result = router.get_rank_key()
    print(result)
    assert 'rand_key' in result
    assert 'key_index' in result


def test_login(router):
    cookies = router.login(username=router.user.username,
                           password=router.user.password)
    print(cookies)
    assert 'Qihoo_360_login' in cookies
    assert 'Token-ID' in cookies
