"""测试 qihoo_360_speedlimit_mixin"""
import pytest

import config


@pytest.fixture(scope='module')
def device():
    """环境变量中的黑名单mac地址"""
    assert len(config.SPEEDLIMIT_LIST) > 0
    device = config.SPEEDLIMIT_LIST[0]
    yield device


def test_set_speed_limit(router, device):
    result = router.set_speed_limit(mac=device.mac,
                                    upload=device.limit_speed,
                                    download=device.limit_speed)
    print(result)
    assert 'err_no' in result and result['err_no'] == '0'


def test_cancel_speed_limit(router, device):
    result = router.cancel_speed_limit(mac=device.mac, )
    print(result)
    assert 'err_no' in result and result['err_no'] == '0'
