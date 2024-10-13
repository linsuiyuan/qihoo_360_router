## 简介
360路由器的一些脚本功能，根据设置的时间段，进行黑名单管理，网络限制速度之类的。

写这个脚本的初衷是为了限制孩子使用电子设备的时间。虽然许多设备有家长控制功能，但是各式各样的不统一，然后孩子有时还会不断试密码，把设备锁住之类的。

有了这个脚本，就可以统一管理了，不管什么设备，需要限制的话，把它加到环境变量里就好了。

唯一的缺点是，需要有一台服务器，或者一台能全天运行的支持运行python脚本的设备。

## 环境变量
需要定义一个 `QIHOO_360` 的环境变量，其格式是一个`json`，相关字段示例如下：
```json
{
  "route_url": "http://192.168.123.1",
  "user": {
    "username": "username",
    "password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  },
  "speedlimits": {
    "default_unlimit_period": [
      "10:00-11:00"
    ],
    "default_limit_speed": 5,
    "device_list": [
      {
        "name": "小米电视",
        "mac": "f0-f0-f0-f0-f0-f0",
        "unlimit_period(可省略字段)": [
          "10:00-11:00"
        ],
        "limit_speed(可省略字段)": 5
      }
    ]
  },
  "blacklists": {
    "default_unblacklist_period": [
      "10:00-11:00"
    ],
    "device_list": [
      {
        "name": "小米电视",
        "mac": "f0-f0-f0-f0-f0-f0",
        "unblacklist_period(可省略字段)": [
          "10:00-11:00"
        ]
      }
    ]
  }
}
```

**注意**：
- 其中`password`字段，前32位是加密的盐，后32位是密码加密后的值。加密函数在`utils.py`文件里
- 可省略的字段，省略的话，将使用相应的默认字段

## 青龙面板部署
- 在`订阅管理`创建相应的订阅，以便把代码拉到青龙里
- 在`环境变量`创建相应的环境变量
- 在`依赖管理`下的`Python3`下面，添加`requirements.txt`里的依赖
- 在`定时任务`里创建相应的定时任务，入口文件是`main.py`

## 存在的问题
### 黑名单管理
不知道是不是使用多个路由器拓扑网络的原因，设置黑名单，再解除黑名单，然后设备有时使用不了WiFi。
需要重启路由，然后才可以正常使用