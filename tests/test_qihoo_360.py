"""测试 qihoo_360"""


def test_get_device_list(qihoo_client):

    devices = qihoo_client.device_list
    for d in devices:
        print(d)

