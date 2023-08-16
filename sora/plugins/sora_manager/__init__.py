import os
import asyncio
import platform

from nonebot import require
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from nonebot.params import ArgStr, ArgPlainText

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.args import Args
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_saa import MessageFactory
from nonebot_plugin_alconna import Match, AlconnaMatch, on_alconna

from sora.utils import __version__, NICKNAME
from sora.permission import BOT_ADMIN, BOT_HELPER
from sora.utils.helpers import HandleCancellation
from sora.utils.update import update, CheckUpdate

__sora_plugin_meta__ = PluginMetadata(
    name="Bot管理",
    description="管理林汐",
    usage="...",
    extra={"author": "KomoriDev", "priority": 1},
)

update_cmd = on_alconna(
    Alconna(
        "更新",
        meta=CommandMeta(
            description="更新林汐",
            usage="@bot /更新",
            example="@bot /更新",
            compact=True,
        ),
    ),
    permission=BOT_HELPER,
    rule=to_me(),
    priority=1,
    block=True,
)
check_update_cmd = on_alconna(
    Alconna(
        "检查更新",
        meta=CommandMeta(
            description="检查更新",
            usage="@bot /检查林汐版本",
            example="@bot /检查更新",
            compact=True,
        ),
    ),
    permission=BOT_HELPER,
    rule=to_me(),
    priority=1,
    block=True,
)

reboot = on_alconna(
    Alconna(
        "重启",
        meta=CommandMeta(
            description="重启林汐",
            usage="@bot /重启",
            example="@bot /重启",
            compact=True,
        ),
    ),
    permission=BOT_ADMIN,
    rule=to_me(),
    priority=1,
    block=True,
)
run_cmd = on_alconna(
    Alconna(
        "cmd",
        Args["cmd", str],
        meta=CommandMeta(
            description="运行终端命令",
            usage="@bot /cmd",
            example="@bot /cmd",
            compact=True,
        ),
    ),
    permission=BOT_ADMIN,
    rule=to_me(),
    priority=1,
    block=True,
)


@update_cmd.handle()
async def _():
    await update_cmd.send(f"{NICKNAME[1]}开始更新", at_sender=True)
    result = await update()
    await MessageFactory(result).send(at_sender=True)
    await update_cmd.finish()


@check_update_cmd.handle()
async def _():
    l_v, l_v_t = await CheckUpdate.show_latest_version()
    if l_v and l_v_t:
        if l_v != __version__:
            await MessageFactory(f"新版本已发布, 请更新\n最新版本: {l_v} 更新时间: {l_v_t}").send(
                at_sender=True
            )
        else:
            await MessageFactory("当前已是最新版本").send(at_sender=True)
    await check_update_cmd.finish()


@reboot.got("flag", prompt=f"确定是否重启{NICKNAME[0]}？确定请回复[是|好|确定]")
async def _(flag: str = ArgStr("flag")):
    if flag.lower() in ["true", "是", "好", "确定", "确定是"]:
        await MessageFactory(f"开始重启{NICKNAME[0]}..请稍等...").send(at_sender=True)
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
async def _(state: T_State, cmd: Match[str] = AlconnaMatch("cmd")):
    if cmd.available:
        state["cmd"] = cmd


@run_cmd.got("cmd", prompt="你输入你要运行的命令", parameterless=[HandleCancellation("已取消")])
async def _(cmd: str = ArgPlainText("cmd")):
    await MessageFactory(f"开始执行{cmd}...").send(at_sender=True)
    p = await asyncio.subprocess.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await p.communicate()
    try:
        result = (stdout or stderr).decode("utf-8")
    except Exception:
        result = str(stdout or stderr)
    await MessageFactory(f"{cmd}\n运行结果：\n{result}").send(at_sender=True)
    await run_cmd.finish()
