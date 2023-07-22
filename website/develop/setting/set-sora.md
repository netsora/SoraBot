---
title: 配置林汐
prev:
  text: "← 准备工作"
  link: "develop/forward/prepare"
next:
  text: "配置Go-cqhttp →"
  link: "develop/setting/set-gocq"
---

# 配置林汐
::: tip
.env* 配置项需符合 dotenv 格式，config.yml 遵循 YAML 语法，如果你不了解 YAML 语法，你可以在[这篇教程](https://www.runoob.com/w3cnote/yaml-intro.html)中学习。
:::
安装 Sora 后会有 `.env` 和 `.env.prod` 文件，它们都是 Sora 的基础配置，在初次启动后会生成 `config.yaml`，其为 Sora 插件配置。

## 申请 QQ频道 机器人
::: tip
如果你不需要它们，只需将 `bot.py` 中对应的代码注释掉

```py
driver.register_adapter(ONEBOT_V11Adapter)
driver.register_adapter(ONEBOT_V12Adapter)
driver.register_adapter(QQGUILD_Adapter) // [!code --]
# driver.register_adapter(QQGUILD_Adapter) // [!code ++]
driver.register_adapter(TG_Adapter)

```

:::
您需要前往 [QQ开放平台](q.qq.com) 注册您的机器人

## 申请 Telegram 机器人
首先你需要有一个 Telegram 帐号，添加 [BotFather](https://t.me/botfather) 为好友。

接着，向它发送 `/newbot` 指令，按要求回答问题。

如果你成功创建了一个机器人，BotFather 会发给你机器人的 token：
```
1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI
```
将这个 token 填入 Bot 的 `env` 文件：
```py
telegram_bots = [{"token": "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI"}]
```
::: tip
如果你需要让你的 Bot 响应除了 `/` 开头之外的消息，你需要向 BotFather 发送 `/setprivacy` 并选择 `Disable`。

如果你需要让你的 Bot 接收 inline query，你还需要向 BotFather 发送 `/setinline`。
:::

### 使用代理
::: tip
如果你的代理使用 socks 协议，你需要安装 httpx[socks]。
:::
如果运行 林汐 的服务器位于中国大陆，那么你可能需要配置代理，否则将无法调用 Telegram 提供的任何 API。
```py
# .dev.prod
PROXY = "···"
```

## 配置详细

### .env.*
打开位于项目根目录的 `.env` 和 `.env.prod` ，你会得到如下内容：（此处展示的为示例填写）

#### .env
```py
ENVIRONMENT=prod
DRIVER=~fastapi+~httpx+~websockets

# 是否为沙盒模式
QQGUILD_IS_SANDBOX=false

# QQ频道机器人帐号
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

# Telegram 机器人账号
telegram_bots = [{"token": "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI"}]
```


#### .env.prod
这个文件没什么好改的，可以直接用
```py
HOST=127.0.0.1
PORT=2310
COMMAND_START=["/","."]
COMMAND_SEP=[" "]
COMMAND_FORCE_WHITESPACE=false
LOG_LEVEL=INFO

NICKNAME=["林汐","Sora"]

# Bot管理员ID
# 启动后，林汐会创建 ID 为 231010 的 Bot管理员账号，并设置密码。您需要输入 /登录 231010 [密码] 来绑定管理员账户
BOT_ADMIN=["231010"]

# Bot协助者ID
# 启动后，林汐会分别创建ID为 666666、233333的 Bot协助者账号，并设置密码。您需要输入 /登录 231010 [密码] 来绑定协助者账户
BOT_HELPER=["666666","233333"]

# 如果使用 Telegram 适配器，请务必填写！
PROXY=""
```

### config.yaml
```yaml 
Award:
  login:        # ---> [20, 10, 0]
    - 20        # 硬币奖励
    - 10        # 好感度奖励
    - 0         # 经验值奖励
  sign:         # ---> [[30, 60], 5, 100]
    - [30, 60]  
    - 5
    - 100

```

* [Award](#award) 为 林汐 奖励机制相关设置

## 解析配置

### Award
* login：       注册奖励
    - 20        硬币奖励
    - 10        好感度奖励
    - 0         经验值奖励
* sign：        注册奖励
    - [30, 60]  硬币奖励 (最小值: 30, 最大值: 60)
    - 5         好感度奖励
    - 100       经验值奖励
