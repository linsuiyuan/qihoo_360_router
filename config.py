"""配置文件"""
import json
import os

# 360路由用户名密码
USERNAME = os.getenv('USERNAME')
assert USERNAME is not None
PASSWORD = os.getenv('PASSWORD')
assert PASSWORD is not None


SPEEDLIMIT_LIST = os.getenv('SPEEDLIMIT_LIST')
assert SPEEDLIMIT_LIST is not None
SPEEDLIMIT_LIST = json.loads(SPEEDLIMIT_LIST)
for d in SPEEDLIMIT_LIST:
    # 由请求获得的mac地址是小写的，这里统一转换为小写
    d['mac'] = d['mac'].lower()
