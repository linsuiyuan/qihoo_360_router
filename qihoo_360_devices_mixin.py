"""360路由设备管理Mixin"""
import requests

from qihoo_360_blacklist_mixin import Qihoo360BlacklistMixin
from qihoo_360_speedlimit_mixin import Qihoo360SpeedlimitMixin


class Qihoo360DevicesMixin(Qihoo360BlacklistMixin, Qihoo360SpeedlimitMixin):
    """360路由设备管理Mixin类，黑名单管理，限速管理等"""

    # noinspection PyMethodMayBeStatic
    def mesh_get_topology_info(self, headers, cookies):
        """获取链接设备列表信息"""

        response = requests.get('http://192.168.123.1/router/mesh_get_topology_info.cgi',
                                cookies=cookies,
                                headers=headers)
        response.raise_for_status()

        route_node = response.json()['data'][0]
        # 如果拓扑节点有链接设备，则拼在同一个列表里
        if route_node['mesh_node']:
            mesh_node = route_node['mesh_node'][0]
            if mesh_node['client_node']:
                route_node['client_node'].extend(mesh_node['client_node'])

        return route_node



