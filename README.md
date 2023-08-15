<div align="center">
  <a href="https://bot.netsora.info/"><img src="https://ghproxy.com/https://raw.githubusercontent.com/netsora/SoraBot/master/resources/logo.jpg" width="200" height="200" 
  style="border-radius: 100px" alt="SoraBot"></a>
</div>

<div align="center">

# SoraBot
_✨ 基于 Nonebot2，互通多平台，超可爱的林汐酱 ✨_
</div>


<p align="center">
<a href="https://raw.githubusercontent.com/netsora/SoraBot/master/LICENSE">
    <img src="https://img.shields.io/github/license/netsora/SoraBot" alt="license">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=edb641" alt="python">
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=edb641" alt="black">
</a>
<a href="https://github.com/Microsoft/pyright">
    <img src="https://img.shields.io/badge/types-pyright-797952.svg?logo=python&logoColor=edb641" alt="pyright">
</a>
<a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<br />
<a href="https://github.com/netsora/SoraBot-website/actions/workflows/website-deploy.yml">
    <img src="https://github.com/netsora/SoraBot-website/actions/workflows/website-deploy.yml/badge.svg?branch=master&event=push" alt="site"/>
</a>
<a href="https://results.pre-commit.ci/latest/github/netsora/SoraBot/master">
    <img src="https://results.pre-commit.ci/badge/github/netsora/SoraBot/master.svg" alt="pre-commit" />
</a>
<a href="https://github.com/netsora/SoraBot/actions/workflows/pyright.yml">
    <img src="https://github.com/netsora/SoraBot/actions/workflows/pyright.yml/badge.svg?branch=master&event=push" alt="pyright">
</a>
<a href="https://github.com/netsora/SoraBot/actions/workflows/ruff.yml">
    <img src="https://github.com/netsora/SoraBot/actions/workflows/ruff.yml/badge.svg?branch=master&event=push" alt="ruff">
</a>
<br />
<a href="https://onebot.dev/">
    <img src="https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="onebot">
</a>
<a href="https://core.telegram.org/bots/api">
    <img src="https://img.shields.io/badge/telegram-Bot-lightgrey?style=social&logo=telegram" alt="telegram">
</a>
<a href="https://bot.q.qq.com/wiki/">
    <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-Bot-lightgrey?style=social&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMTIuODIgMTMwLjg5Ij48ZyBkYXRhLW5hbWU9IuWbvuWxgiAyIj48ZyBkYXRhLW5hbWU9IuWbvuWxgiAxIj48cGF0aCBkPSJNNTUuNjMgMTMwLjhjLTcgMC0xMy45LjA4LTIwLjg2IDAtMTkuMTUtLjI1LTMxLjcxLTExLjQtMzQuMjItMzAuMy00LjA3LTMwLjY2IDE0LjkzLTU5LjIgNDQuODMtNjYuNjQgMi0uNTEgNS4yMS0uMzEgNS4yMS0xLjYzIDAtMi4xMy4xNC0yLjEzLjE0LTUuNTcgMC0uODktMS4zLTEuNDYtMi4yMi0yLjMxLTYuNzMtNi4yMy03LjY3LTEzLjQxLTEtMjAuMTggNS40LTUuNTIgMTEuODctNS40IDE3LjgtLjU5IDYuNDkgNS4yNiA2LjMxIDEzLjA4LS44NiAyMS0uNjguNzQtMS43OCAxLjYtMS43OCAyLjY3djQuMjFjMCAxLjM1IDIuMiAxLjYyIDQuNzkgMi4zNSAzMS4wOSA4LjY1IDQ4LjE3IDM0LjEzIDQ1IDY2LjM3LTEuNzYgMTguMTUtMTQuNTYgMzAuMjMtMzIuNyAzMC42My04LjAyLjE5LTE2LjA3LS4wMS0yNC4xMy0uMDF6IiBmaWxsPSIjMDI5OWZlIi8+PHBhdGggZD0iTTMxLjQ2IDExOC4zOGMtMTAuNS0uNjktMTYuOC02Ljg2LTE4LjM4LTE3LjI3LTMtMTkuNDIgMi43OC0zNS44NiAxOC40Ni00Ny44MyAxNC4xNi0xMC44IDI5Ljg3LTEyIDQ1LjM4LTMuMTkgMTcuMjUgOS44NCAyNC41OSAyNS44MSAyNCA0NS4yOS0uNDkgMTUuOS04LjQyIDIzLjE0LTI0LjM4IDIzLjUtNi41OS4xNC0xMy4xOSAwLTE5Ljc5IDAiIGZpbGw9IiNmZWZlZmUiLz48cGF0aCBkPSJNNDYuMDUgNzkuNThjLjA5IDUgLjIzIDkuODItNyA5Ljc3LTcuODItLjA2LTYuMS01LjY5LTYuMjQtMTAuMTktLjE1LTQuODItLjczLTEwIDYuNzMtOS44NHM2LjM3IDUuNTUgNi41MSAxMC4yNnoiIGZpbGw9IiMxMDlmZmUiLz48cGF0aCBkPSJNODAuMjcgNzkuMjdjLS41MyAzLjkxIDEuNzUgOS42NC01Ljg4IDEwLTcuNDcuMzctNi44MS00LjgyLTYuNjEtOS41LjItNC4zMi0xLjgzLTEwIDUuNzgtMTAuNDJzNi41OSA0Ljg5IDYuNzEgOS45MnoiIGZpbGw9IiMwODljZmUiLz48L2c+PC9nPjwvc3ZnPg==" alt="QQ频道">
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
  <a href="https://bot.netsora.info/module/">服务列表</a>
  ·
  <a href="https://bot.netsora.info/guide/before/prepare">安装文档</a>
  ·
  <a href="https://sorabot.netlify.app/">文档打不开?</a>
</p>

## 简介
> **Note**  
> 一切开发旨在学习，请勿用于非法用途

林汐（SoraBot）基于 Nonebot2 开发，互通多平台，以 sqlite3 作为数据库的功能型机器人

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
* [`nonebot/noenbot2`](https://github.com/netsora/SoraBot)：跨平台Python异步机器人框架  
* [`Mrs4s/go-cqhttp`](https://github.com/Mrs4s/go-cqhttp)：cqhttp的golang实现，轻量、原生跨平台.  
* [`Kyomotoi/ATRI`](https://github.com/Kyomotoi/ATRI)：高性能文爱萝卜子
* [`HibiKier/zhenxun_bot`](https://github.com/HibiKier/zhenxun_bot)：非常可爱的绪山真寻bot
* [`CMHopeSunshine/LittlePaimon`](https://github.com/CMHopeSunshine/LittlePaimon)：原神Q群机器人
* [`nonebot_plugin_saa`](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere)：多适配器消息发送支持
* [`nonebot_plugin_alconna`](https://github.com/nonebot/plugin-alconna)：强大的 Nonebot2 命令匹配拓展

## 许可证
本项目使用 AGPLv3.

意味着你可以运行本项目，并向你的用户提供服务。除非获得商业授权，否则无论以何种方式修改或者使用代码，都需要开源
