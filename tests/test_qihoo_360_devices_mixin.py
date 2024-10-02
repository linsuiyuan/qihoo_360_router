"""测试 qihoo_360_devices_mixin"""
import json


def test_mesh_get_topology_info(qihoo_client):
    data = qihoo_client.mesh_get_topology_info()
    print(json.dumps(data))
