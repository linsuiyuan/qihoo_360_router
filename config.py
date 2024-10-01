"""配置文件"""
import json
import os
from urllib import parse

# 360路由用户名密码
QIHOO_USER = os.getenv('QIHOO_USER')
QIHOO_USER = parse.parse_qs(QIHOO_USER)

USERNAME = QIHOO_USER['USERNAME'][0]
assert USERNAME is not None
PASSWORD = QIHOO_USER['PASSWORD'][0]
assert PASSWORD is not None


SPEEDLIMIT_LIST = os.getenv('QIHOO_SPEEDLIMIT_LIST')
assert SPEEDLIMIT_LIST is not None
SPEEDLIMIT_LIST = json.loads(SPEEDLIMIT_LIST)
for d in SPEEDLIMIT_LIST:
    # 由请求获得的mac地址是小写的，这里统一转换为小写
    d['mac'] = d['mac'].lower()
