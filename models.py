"""一些数据类"""
from dataclasses import dataclass


@dataclass
class Qihoo360Device:
    """360路由连接设备类"""
    # 设备mac地址
    mac: str
    # 设备ip
    ip: str
    # 速度限制标志
    limit_enable: int
    limit_up_speed: int
    limit_down_speed: int
    second: int
    login_time: int
    # 设备名称，一般是英文的
    name: str
    # 设备标签，一般是中文
    device_label: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Qihoo360Device':
        """从字典中创建实例"""
        # 使用字典解包，提供默认值
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})  # noqa
