import os
import asyncio
import platform

from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot import require, on_command
from nonebot.plugin import PluginMetadata
from nonebot.internal.adapter import Message
from nonebot.params import ArgStr, CommandArg, ArgPlainText
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

require("nonebot_plugin_saa")
from sora.utils import NICKNAME
from sora.permission import BOT_ADMIN, BOT_HELPER
from sora.utils.update import update, check_update

__sora_plugin_meta__ = PluginMetadata(
    name="Bot管理",
    description="管理林汐",
    usage="...",
    extra={"author": "KomoriDev", "priority": 1},
)

update_cmd = on_command(
    "更新",
    permission=BOT_HELPER,
    rule=to_me(),
    priority=1,
    block=True,
    state={
        "name": "bot_update",
        "description": "从Git中更新bot，需 Bot协助者 权限",
        "usage": "@bot 更新",
        "priority": 1,
    },
)
check_update_cmd = on_command(
    "检查更新",
    permission=BOT_HELPER,
    rule=to_me(),
    priority=1,
    block=True,
    state={
        "name": "bot_check_update",
        "description": "从Git检查bot更新情况，需 Bot协助者 权限",
        "usage": "@bot 检查更新",
        "priority": 1,
    },
)

reboot = on_command(
    cmd="重启",
    permission=BOT_ADMIN,
    rule=to_me(),
    priority=1,
    block=True,
    state={
        "name": "bot_restart",
        "description": "执行重启操作，需 Bot管理员 权限",
        "usage": "@bot /重启",
        "priority": 1,
    },
)
run_cmd = on_command(
    cmd="cmd",
    permission=BOT_ADMIN,
    rule=to_me(),
    priority=1,
    block=True,
    state={
        "name": "bot_cmd",
        "description": "运行终端命令，需 Bot管理员 权限",
        "usage": "@bot cmd<命令>",
        "priority": 1,
    },
)


@update_cmd.handle()
async def _(event: V11MessageEvent | GuildMessageEvent | TGMessageEvent):
    await update_cmd.send(f"{NICKNAME[1]}开始更新", at_sender=True)
    result = await update()
    await update_cmd.finish(result, at_sender=True)


@check_update_cmd.handle()
async def _(event: V11MessageEvent | GuildMessageEvent | TGMessageEvent):
    result = await check_update()
    await check_update_cmd.finish(result, at_sender=True)


@reboot.got("flag", prompt=f"确定是否重启{NICKNAME[1]}？确定请回复[是|好|确定]")
async def _(flag: str = ArgStr("flag")):
    if flag.lower() in ["true", "是", "好", "确定", "确定是"]:
        await reboot.send(f"开始重启{NICKNAME}..请稍等...")
        open("is_restart", "w")
        if str(platform.system()).lower() == "windows":
            import sys

            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            os.system("./restart.sh")
    else:
        await reboot.send("已取消操作...")


@run_cmd.handle()
async def _(event: V11MessageEvent | GuildMessageEvent | TGMessageEvent, state: T_State, cmd: Message = CommandArg()):
    if cmd:
        state["cmd"] = cmd


@run_cmd.got("cmd", prompt="你输入你要运行的命令")
async def _(event: V11MessageEvent | GuildMessageEvent | TGMessageEvent, cmd: str = ArgPlainText("cmd")):
    await run_cmd.send(f"开始执行{cmd}...", at_sender=True)
    p = await asyncio.subprocess.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await p.communicate()
    try:
        result = (stdout or stderr).decode("utf-8")
    except Exception:
        result = str(stdout or stderr)
    await run_cmd.finish(f"{cmd}\n运行结果：\n{result}")
