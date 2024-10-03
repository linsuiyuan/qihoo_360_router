"""测试 qihoo_360_blacklist_mixin"""
import json

import pytest

import config


@pytest.fixture(scope='module')
def mac():
    """环境变量中的黑名单mac地址"""
    assert len(config.BLACKLISTS) > 0
    blacklist = config.BLACKLISTS[0]
    assert 'mac' in blacklist
    yield blacklist['mac']


def test_get_blacklist(router):
    result = router.get_blacklist()
    # print(json.dumps(result))
    assert 'err_no' in result and result['err_no'] == '0'


def test_set_blacklist(router, mac):
    result = router.set_blacklist(mac=mac)
    # print(json.dumps(result))
    assert 'err_no' in result and result['err_no'] == '0'
    is_in_blacklist = router.is_in_blacklist(mac)
    assert is_in_blacklist is True


def test_cancel_blacklist(router, mac):
    result = router.cancel_blacklist(mac=mac)
    # print(json.dumps(result))
    assert 'err_no' in result and result['err_no'] == '0'
    is_in_blacklist = router.is_in_blacklist(mac)
    assert is_in_blacklist is False
