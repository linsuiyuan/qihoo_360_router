"""测试 qihoo_360_blacklist_mixin"""
import config


def test_get_blacklist(qihoo_client):
    result = qihoo_client.get_blacklist()
    print(f'{test_get_blacklist.__name__} result: {result}')
    assert 'err_no' in result and result['err_no'] == '0'


def test_set_blacklist(qihoo_client):
    mac = config.SPEEDLIMIT_LIST[0]['mac']
    result = qihoo_client.set_blacklist(mac=mac)
    print(result)
    assert 'err_no' in result and result['err_no'] == '0'


def test_cancel_blacklist(qihoo_client):
    mac = config.SPEEDLIMIT_LIST[0]['mac']
    result = qihoo_client.cancel_blacklist(mac=mac)
    print(result)
    assert 'err_no' in result and result['err_no'] == '0'
