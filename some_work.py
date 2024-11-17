"""一些手动执行的功能"""
import config
from qihoo_360 import Qihoo360


def sync_virtual_service():
    """同步端口映射"""
    qihoo = Qihoo360(username=config.USER.username,
                     password=config.USER.password)

    env_vs_list = config.QIHOO_360_VIRTUAL_SERVICES

    # 清除全部端口映射
    result = qihoo.virtual_service_clean()
    print(f"清除全部端口映射结果：{result}")

    for vs in env_vs_list:
        print(f"添加端口映射：{vs}")
        result = qihoo.virtual_service_add(name=vs.name,
                                           internal_ip=vs.internal_ip,
                                           external_port=vs.external_port,
                                           internal_port=vs.internal_port)
        print(f"添加结果：{result}")


if __name__ == '__main__':
    sync_virtual_service()
