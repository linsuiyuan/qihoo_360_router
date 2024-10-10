"""测试 qihoo_360"""


def test_get_device_list(router):

    devices = router.device_list
    for d in devices:
        print(d)
