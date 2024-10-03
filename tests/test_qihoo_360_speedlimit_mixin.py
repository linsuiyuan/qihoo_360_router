"""测试 qihoo_360_speedlimit_mixin"""
import config


def test_set_speed_limit(router):
    mac = config.SPEEDLIMIT_LIST[0]['mac']
    upload = 10
    download = 10
    result = router.set_speed_limit(mac=mac,
                                    upload=upload,
                                    download=download)
    print(result)
    assert 'err_no' in result and result['err_no'] == '0'


def test_cancel_speed_limit(router):
    mac = config.SPEEDLIMIT_LIST[0]['mac']
    result = router.cancel_speed_limit(mac=mac, )
    print(result)
    assert 'err_no' in result and result['err_no'] == '0'
