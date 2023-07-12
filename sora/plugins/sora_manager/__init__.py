import os
import platform

from nonebot.rule import to_me
from nonebot.params import ArgStr
from nonebot import require, on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent as GroupMessageEvent

require("nonebot_plugin_saa")
from sora.utils import NICKNAME
from sora.permission import BOT_ADMIN

__sora_plugin_meta__ = PluginMetadata(
    name="Bot管理",
    description="管理林汐",
    usage="...",
    extra={"author": "mute.", "priority": 1},
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


@reboot.got("flag", prompt=f"确定是否重启{NICKNAME}？确定请回复[是|好|确定]")
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
