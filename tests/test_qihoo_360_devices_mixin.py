"""测试 qihoo_360_devices_mixin"""
import json

from qihoo_360_devices_mixin import Qihoo360DevicesMixin


def test_mesh_get_topology_info(qihoo_client):
    mixin = Qihoo360DevicesMixin()

    data = mixin.mesh_get_topology_info(headers=qihoo_client.headers,
                                        cookies=qihoo_client.cookies
                                        )
    print(json.dumps(data))
