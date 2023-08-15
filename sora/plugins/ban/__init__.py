from nonebot import require
from nonebot.rule import to_me
from nonebot.internal.adapter import Bot
from nonebot.internal.adapter import Event

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.args import Args
from arclet.alconna.base import Option
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import Match, on_alconna, AlconnaMatch
from nonebot_plugin_alconna.adapters import At
from nonebot_plugin_saa import MessageFactory

from sora.log import logger
from sora.database import BanUser
from sora.utils.user import get_bind_info
from sora.permission import BOT_HELPER, get_helper_list


ban = on_alconna(
    Alconna(
        "ban",
        Option(
            "add",
            Args["target", At | int]["hours?", int]["minutes?", int],
            help_text="封禁用户",
        ),
        Option("remove", Args["target", At | int], help_text="解封用户"),
        Option("-l|--list", help_text="查询所有被封禁用户"),
        meta=CommandMeta(
            description="你被逮捕了！丢进小黑屋！",
            usage="@bot /ban <at | user_id> [小时] [分钟]",
            example="""
            @bot /ban add @user
            @bot /ban add 2023081136 2
            @bot /ban add @user 2 30
            @bot /ban remove @user
            @bot /ban -l
            """,
            compact=True,
        ),
    ),
    priority=5,
    block=True,
    rule=to_me(),
    permission=BOT_HELPER,
)


@ban.assign("add")
async def add(
    bot: Bot,
    event: Event,
    banUser: Match[At | int] = AlconnaMatch("target"),
    hours: Match[int] = AlconnaMatch("hours"),
    minutes: Match[int] = AlconnaMatch("minutes"),
):
    if isinstance(banUser.result, At):
        target = banUser.result.target
        if target == bot.self_id:
            await MessageFactory("你的权限不够喔").send(at_sender=True)
            await ban.finish()
        target_id = (await get_bind_info(event, target)).user_id
    else:
        target_id = banUser.result

    if target_id in await get_helper_list():
        await MessageFactory("你的权限不够喔").send(at_sender=True)
        await ban.finish()

    if hours.available:
        if minutes.available:
            minutes_result = minutes.result
        else:
            minutes_result = 0
        hours_result = hours.result
        logger.info("封禁", f"封禁目标：{target_id}，时长：{hours_result}小时{minutes_result}分钟")
        await BanUser.ban(
            target_id, duration=convert_to_seconds(hours_result, minutes_result)
        )
        await MessageFactory(
            f"已成功封禁用户：{target_id}，时长：{hours_result}小时{minutes_result}分钟"
        ).send(at_sender=True)
    else:
        logger.info("封禁", f"永久封禁目标：{target_id}")
        await BanUser.ban(target_id, duration=-1)
        await MessageFactory(f"已永久封禁用户：{target_id}").send(at_sender=True)

    await ban.finish()


@ban.assign("remove")
async def remove(
    bot: Bot, event: Event, banUser: Match[At | int] = AlconnaMatch("target")
):
    if isinstance(banUser.result, At):
        target = banUser.result.target
        if target == bot.self_id:
            await MessageFactory("你的权限不够喔").send(at_sender=True)
            await ban.finish()
        target_id = (await get_bind_info(event, target)).user_id
    else:
        target_id = banUser.result

    if target_id in await get_helper_list():
        await MessageFactory("你的权限不够喔").send(at_sender=True)
        await ban.finish()

    await BanUser.unban(target_id)
    logger.info("封禁", f"解除封禁：{target_id}")
    await MessageFactory(f"已解除封禁：{target_id}").send(at_sender=True)

    await ban.finish()


@ban.assign("list")
async def list():
    ban_users = await BanUser.all()
    if ban_users:
        message = "\n".join(
            [
                f"ID: {ban_user.id}\n"
                f"用户ID: {ban_user.user_id}\n"
                f"封禁开始时间: {ban_user.ban_time}\n"
                f"封禁时长: {ban_user.duration}\n"
                for ban_user in ban_users
            ]
        )
    else:
        message = "当前还没有被封禁用户呢"
    await MessageFactory(message).send(at_sender=True)


def convert_to_seconds(hours: int, minutes: int):
    total_minutes = hours * 60 + minutes
    total_seconds = total_minutes * 60
    return total_seconds
