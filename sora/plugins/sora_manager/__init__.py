import os
import sys
import random
import asyncio
import contextlib
from pathlib import Path
from typing import Union

from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from nonebot import get_app, require, on_command
from nonebot.internal.adapter import Bot, Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import ActionFailed as V11ActionFailed
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.onebot.v11 import GroupMessageEvent as GroupMessageEvent
from nonebot.adapters.qqguild.exception import ActionFailed as GuildActionFailed

require("nonebot_plugin_saa")
from sora.utils import NICKNAME
from sora.utils.files import save_json
from nonebot_plugin_saa import MessageFactory
from sora.permission import BOT_ADMIN, BOT_HELPER

__sora_plugin_meta__ = PluginMetadata(
    name="Bot管理",
    description="管理林汐",
    usage="...",
    extra={"author": "mute.", "priority": 1},
)

reboot_cmd = on_command(
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
    "cmd",
    permission=BOT_ADMIN,
    rule=to_me(),
    priority=5,
    block=True,
    state={
        "name": "bot_cmd",
        "description": "运行终端命令，需超级用户权限",
        "usage": "@bot cmd<命令>",
        "priority": 5,
    },
)
broadcast = on_command(
    "广播",
    permission=BOT_HELPER,
    rule=to_me(),
    priority=5,
    block=True,
    state={
        "name": "broadcast",
        "description": "向指定或所有群发送消息，需大于 Bot协助者 权限",
        "usage": "@bot 广播<内容>",
        "priority": 5,
    },
)


@reboot_cmd.handle()
async def _(bot: Bot, event: Union[V11MessageEvent, GuildMessageEvent]):
    await MessageFactory(f"{NICKNAME}开始执行重启，请等待我的归来").send(at_sender=True)
    await reboot_cmd.send()

    if isinstance(event, GroupMessageEvent):
        session_id = event.group_id
    elif isinstance(event, GuildMessageEvent):
        session_id = event.guild_id
    else:
        session_id = event.user_id
    reboot_data = {
        "session_type": event.message_type,
        "session_id": session_id,
        "message_card": {},
    }

    save_json(reboot_data, Path() / "rebooting.json")
    with contextlib.suppress(Exception):
        await get_app().router.shutdown()
    reboot_arg = (
        [sys.executable] + sys.argv
        if sys.argv[0].endswith(".py")
        else [sys.executable, "bot.py"]
    )
    os.execv(sys.executable, reboot_arg)


@run_cmd.handle()
async def _(
    event: Union[V11MessageEvent, GuildMessageEvent],
    state: T_State,
    cmd: Message = CommandArg(),
):
    if cmd:
        state["cmd"] = cmd


@run_cmd.got("cmd", prompt="你输入你要运行的命令")
async def _(
    event: Union[V11MessageEvent, GuildMessageEvent], cmd: str = ArgPlainText("cmd")
):
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


@broadcast.handle()
async def _(
    event: Union[V11MessageEvent, GuildMessageEvent],
    state: T_State,
    msg: Message = CommandArg(),
):
    if msg:
        state["msg"] = msg
    else:
        await broadcast.finish("请给出要广播的消息", at_sender=True)


@broadcast.got("groups", prompt="要广播到哪些群呢？多个群以空格隔开，或发送 [/全部] 向所有群广播")
async def _(
    event: Union[V11MessageEvent, GuildMessageEvent],
    bot: Bot,
    msg: Message = Arg("msg"),
    groups: str = ArgPlainText("groups"),
):
    group_list = await bot.get_group_list()
    group_list = [g["group_id"] for g in group_list]
    if groups in {"全部", "所有", "all"}:
        send_groups = group_list
    else:
        groups = groups.split(" ")
        send_groups = [
            int(group)
            for group in groups
            if group.isdigit() and int(group) in group_list
        ]
    if not send_groups:
        await broadcast.finish("要广播的群未加入或参数不对", at_sender=True)
    else:
        await broadcast.send(f"开始向{len(send_groups)}个群发送广播，每群间隔5~10秒", at_sender=True)
        for group in send_groups:
            try:
                await bot.send_group_msg(group_id=group, message=msg)
                await asyncio.sleep(random.randint(5, 10))
            except V11ActionFailed:
                await broadcast.send(f"群{group}发送消息失败")
        await broadcast.finish("消息广播发送完成", at_sender=True)
