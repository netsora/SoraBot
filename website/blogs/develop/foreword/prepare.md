---
title: 准备工作
date: 2023-06-11
categories:
 - 安装
 - 指北
tags:
 - 安装
---

# 准备工作
::: danger
Sora 不支持使用 nb-cli 控制，请勿使用 nb-cli 操作或管理 SoraBot  
后续会开发 sora-cli 来辅助开发者（也许？
:::

## 前言
~~林汐非常可爱的帕~~

**什么是 SoraBot**  
SoraBot(林汐) 是基于 Nonebot2 和 go-cqhttp 开发的机器人

**我为什么需要 go-cqhttp**  
SoraBot 本身只负责处理消息，需要借助 go-cqhttp 与 QQ 进行通信。  

同时 SoraBot 仅使用 go-cqhttp 进行测试。使用其他 OneBot 实现（如 [OneBot Kotlin](https://github.com/yyuueexxiinngg/onebot-kotlin)），请自行承担可能存在的兼容性问题。

**门槛**  

在开始之前，我们希望您具备：
* 一定的基础，包括但不限于稍微熟悉linux或windows cmd命令行
* 一些百度/Google的能力
* 一台服务器或能 24 小时运行的电脑

## 你可能会问
**什么是独立ID，它有什么用？**  
独立ID是林汐为每个用户分配的专属ID，通过它，我们便可知晓用户信息、绑定信息、权限等，以便我们更好向用户提供服务

**全新的权限系统，新在哪里？**  
林汐的权限系统，并没有使用 Nonebot2 所提供的 `SUPERUSER`，而是改为了 `Bot管理员` 和 `Bot协助者`

::: danger 
请不要将 Bot管理员ID 重复设置在 Bot协助者中。事实上，Bot协助者本就包括Bot管理员
:::
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


## 环境准备
::: tip
请确保你的 Python 版本 >= 3.8
:::
为了让 Sora 稳定运行，我们使用了虚拟环境（[Poetry](https://python-poetry.org/)）
```bash
# 安装 python 依赖
poetry install
# 安装 pre-commit git hook
pre-commit install
```

## 本体准备

### 通过 Git 下载 Sora
在任意你喜欢的目录下键入：
:::: code-group
::: code-group-item HTTPS
```bash
git clone https://github.com/netsora/SoraBot.git
```
:::
::: code-group-item SSH
```bash
git clone git@github.com:netsora/SoraBot.git
```
:::
::: code-group-item Github CLI
```bash
gh repo clone netsora/SoraBot
```
:::
::::


### 通过 GitHub Codespaces 使用 Sora
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=master&repo=645755460)

### 通过 Gitpod 使用 Sora
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#/https://github.com/netsora/SoraBot)

### 通过其它方法下载 Sora
1. 进入 [Sora 主仓库](https://github.com/netsora/SoraBot)
2. 点击显眼的**绿色**按钮：Code
3. 在出现的菜单中找到 Download ZIP 并点击
4. 下载完成后解压至任一你喜欢的目录
