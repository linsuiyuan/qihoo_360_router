## 简介
360路由器的一些脚本功能，根据设置的时间段，进行黑名单管理，网络限制速度之类的

## 环境变量
需要定义一个 `QIHOO_360` 的环境变量，其格式是一个`json`，相关字段示例如下：
```json
{
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

**注意**：其中`password`字段，前32位是加密的盐，后32位是密码加密后的值

## 存在的问题
### 黑名单管理
不知道是不是使用多个路由器拓扑网络的原因，设置黑名单，然后解除黑名单，然后设备还是使用不了WiFi（从路由）。
需要对从路由进行重启，然后才可以正常使用