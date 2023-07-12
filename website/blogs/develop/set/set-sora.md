---
title: 配置 SoraBot
date: 2023-06-11
categories:
 - 安装
 - 指北
tags:
 - 安装
---

# 配置 SoraBot
::: tip
.env* 配置项需符合 dotenv 格式，config.yml 遵循 YAML 语法，如果你不了解 YAML 语法，你可以在[这篇教程](https://www.runoob.com/w3cnote/yaml-intro.html)中学习。
:::
安装 Sora 后会有 .env 和 .env.prod 文件，它们都是 Sora 的基础配置，在初次启动后会生成 config.yaml，其为 Sora 插件配置。


## 配置详细

### .env.*
打开位于项目根目录的 `.env` 和 `.env.prod` ，你会得到如下内容：（此处展示的为示例填写）

#### .env
```py
ENVIRONMENT=prod
DRIVER=~fastapi+~httpx+~websockets

# 是否为沙盒模式
QQGUILD_IS_SANDBOX=false

# 机器人帐号
QQGUILD_BOTS='
[
    {
        "id": "xxx",
        "token": "xxx",
        "secret": "xxx",
        "intent": {
            "guild_messages": false,
            "at_messages": true
        }   
    }
]
```
您需要前往 [QQ开放平台](q.qq.com) 注册您的机器人

#### .env.prod
这个文件没什么好改的，可以直接用
```py
HOST=127.0.0.1
PORT=2310
COMMAND_START=["/","."]
COMMAND_SEP=[" "]

LOG_LEVEL=INFO

NICKNAME=["林汐","Sora"]

# Bot管理员ID
# 启动后，林汐会创建 ID 为 231010 的 Bot管理员账号，并设置密码。您需要输入 /登录 231010 [密码] 来绑定管理员账户
BOT_ADMIN=["231010"]

# Bot协助者ID
# 启动后，林汐会分别创建ID为 666666、233333的 Bot协助者账号，并设置密码。您需要输入 /登录 231010 [密码] 来绑定协助者账户
BOT_HELPER=["666666","233333"]

PROXY=""
```

### config.yaml
```yaml 

WithGoCQHTTP:
  enabled: true
  accounts:
    - uin: 1145141919
      password: "1919810"
      protocol: 1
  
  download_domain: "{download_domain}"
  download_version: "v1.1.0"

  gocq_webui_username: "sora"
  gocq_webui_password: "sora2333***"
```

* [WithGoCQHTTP](#withgocqhttp) 为内置 gocqhttp 相关设置

## 解析配置
### WithGoCQHTTP
* enabled：是否启用。
* accounts：需要登陆的账号，如不会填写，启用后前往：http://{host}:{port}/go-cqhttp/ 配置即可。
    - uin：🐧账号。
    - password：登录密码。
    - protocol：登录设备类型。
* download_domain：gocqhttp 下载域名，可选：github.com、download.fastgit.org、ghdown.obfs.dev。
* download_version：gocqhttp 下载版本。
* gocq_webui_username：内置 gocqhttp WebUI 的登录凭证：账号。
* gocq_webui_password：内置 gocqhttp WebUI 的登录凭证：密码。
::: details protocol
| 值 | 类型 | 限制 |
| :---: | :---: | :---: |
| 0 | Default/Unset | 当前版本下默认为iPad |
| 1 | Android Phone | 无 |
| 2 | Android Watch | 无法接收 notify 事件、无法接收口令红包、无法接收撤回消息 |
| 3 | MacOS | 无 |
| 4 | 企点 | 只能登录企点账号或企点子账号 |
| 5 | iPad | 无 |
| 6 | aPad | 无 |
:::
