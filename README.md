<div align="center">
  <a href="https://bot.netsora.info/"><img src="./resources/logo.png" width="200" height="200" 
  style="border-radius: 100px" alt="SoraBot"></a>
</div>

<div align="center">

# SoraBot
_✨ 基于 Nonebot2 和 go-cqhttp 开发，超可爱的林汐酱 ✨_
</div>


<p align="center">
<a href="https://raw.githubusercontent.com/netsora/SoraBot/master/LICENSE">
    <img src="https://img.shields.io/github/license/netsora/SoraBot" alt="license">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue" alt="python">
<a href="https://github.com/netsora/SoraBot/releases">
  <img src="https://img.shields.io/github/v/release/netsora/SoraBot" alt="release"/>
</a>
<a href="https://results.pre-commit.ci/latest/github/netsora/SoraBot/master">
  <img src="https://results.pre-commit.ci/badge/github/netsora/SoraBot/nonebot2/master.svg" alt="pre-commit" />
</a>
<a href="https://bot.netsora.info/">
  <img src="https://api.netlify.com/api/v1/badges/7dfd5fe6-d423-4f55-a6fc-02753f07e9e9/deploy-status" alt="netlify-status" />
</a>
</br>
<a href="http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=A9oTio04Frz8oX0WgbPWM9OszLcF5RHT&authKey=D84U3cnB2Lax1qgww4psT1OgEU1iOOKW4evsdhnQuHtV3QFedQGNNLm1kK2Mfj15&noverify=0&group_code=817451732">
  <img src="https://img.shields.io/badge/QQ%E7%BE%A4-817451732-orange?style=flat-square" alt="QQ Chat Group">
</a>
<a href="https://pd.qq.com/s/5b26z878f">
  <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-林汐咖啡屋-5492ff?style=flat-square" alt="QQ Channel">
</a>
<!-- <a href="https://discord.gg/YRVwvYt58X">
  <img src="https://discord.com/api/guilds/1113846954955378868/widget.png?style=shield" alt="Discord Server">
</a> -->
</p>

<p align="center">
  <a href="https://bot.netsora.info/">文档</a>
  ·
  <a href="https://bot.netsora.info/docs/module/">服务列表</a>
  ·
  <a href="https://bot.netsora.info/blogs/develop/foreword/prepare.html">安装文档</a>
</p>

## 简介
> **Note**  
> 一切开发旨在学习，请勿用于非法用途

林汐（SoraBot）基于 Nonebot2 和 go-cqhttp 开发，以 sqlite3 作为数据库的功能型机器人

## 特色
* 使用 NoneBot2 进行项目底层构建.
* 使用 go-cqhttp 作为默认协议端.
* 互通 QQ、QQ频道、Telegram 等平台
* 独立ID，更方便管理与互通数据
* 全新的权限系统，不用重启便可自定义 Bot管理员 和 Bot协助者
* Coming soon...

## 你可能会问
**什么是独立ID，它有什么用？**  
独立ID是林汐为每个用户分配的专属ID，通过它，我们便可知晓用户信息、绑定信息、权限等，以便我们更好向用户提供服务

**全新的权限系统，新在哪里？**  
林汐的权限系统，并没有使用 Nonebot2 所提供的 `SUPERUSER`，而是改为了 `Bot管理员` 和 `Bot协助者`
> **Warning**  
> 请不要将 Bot管理员ID 重复设置在 Bot协助者中。事实上，Bot协助者本就包括Bot管理员
```py
# Bot管理员ID
# 启动后，林汐会创建 ID 为 231010 的 Bot管理员账号，并设置密码。您需要输入 /登录 231010 [密码] 来绑定管理员账户
BOT_ADMIN=["231010"]

# Bot协助者ID
# 启动后，林汐会分别创建ID为 666666、233333的 Bot协助者账号，并设置密码。您需要输入 /登录 231010 [密码] 来绑定协助者账户
BOT_HELPER=["666666","233333"]
```
启动后，林汐会自动为他们注册账号及密码，并设置权限。  


**Bot管理员 和 Bot协助者 的区别是？**  
Bot管理员是最高权限， 拥有 Bot协助者 的权限，所以我们便可以说 Bot协助者 包括 Bot管理员

<details>
<summary>Example</summary>

`/重启` 指令只能由 Bot管理员 触发
```python
reboot_cmd = on_command(
    cmd='重启',
    permission=BOT_ADMIN
)
```

`/重启` 指令可以由 Bot管理员 和 Bot协助者 触发
```python
reboot_cmd = on_command(
    cmd='重启',
    permission=BOT_HELPER
)
```
</details>

## 更新日志

版本更新请参考[此处](./CHANGELOG.md).

小改动请参考以往的 [commit](https://github.com/netsora/SoraBot/commit/master).

## 贡献
如果你喜欢本项目，可以请我[喝杯快乐水](https://afdian.net/@netsora)

如果你有想法、有能力，欢迎：  

* [提交 Issue](https://github.com/netsora/SoraBot/issues)
* [提交 Pull request](https://github.com/netsora/SoraBot/pulls)  
* [在交流群内反馈](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=kUsNnKC-8F_YnR6VvYGqDiZOmhSi-iw7&authKey=IlG5%2FP1LrCVfniACFmdKRRW1zXq6fto5a43vfAHBqC5dUNztxLRuJnrVou2Q8UgH&noverify=0&group_code=817451732)

请参考 [贡献指南](./CONTRIBUTING.md)

## 鸣谢
感谢以下 开发者 和 Github项目 对 SoraBot 作出的贡献：（排名不分先后）
* [`nonebot/noenbot2`](https://github.com/nonebot/nonebot2)：跨平台Python异步机器人框架  
* [`Mrs4s/go-cqhttp`](https://github.com/Mrs4s/go-cqhttp)：cqhttp的golang实现，轻量、原生跨平台.  
* [`Kyomotoi/ATRI`](https://github.com/Kyomotoi/ATRI)：高性能文爱萝卜子
* [`CMHopeSunshine/LittlePaimon`](https://github.com/CMHopeSunshine/LittlePaimon)：原神Q群机器人
* [`nonebot_plugin_saa`](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere)：多适配器消息发送支持

## 许可证
本项目使用 AGPLv3.

意味着你可以运行本项目，并向你的用户提供服务。除非获得商业授权，否则无论以何种方式修改或者使用代码，都需要开源
