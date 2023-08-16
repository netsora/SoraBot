from typing import Annotated

from nonebot import require
from nonebot.rule import to_me

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")

from arclet.alconna.args import Args
from arclet.alconna.core import Alconna
from arclet.alconna.base import Option, Subcommand
from arclet.alconna.config import namespace
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import Query, Match, on_alconna, AlconnaMatch, AlconnaQuery
from nonebot_plugin_saa import MessageFactory

from sora.log import logger
from sora.utils import DRIVER
from sora.utils.api import random_text
from sora.utils.user import getUserInfo
from sora.database.models import UserInfo
from sora.permission import get_admin_list, get_helper_list


authorize: str = ""

__usage__ = """
USER
查看 Bot管理员 列表：/admin -l

BOT_ADMIN
初始化权限：/admin -i <token>
增加管理员：/admin add -a <user_id>
增加协助者：/admin add -h <user_id>
取消管理员：/admin remove -a <user_id>
取消协助者：/admin remove -h <user_id>
"""

with namespace("Sora") as ns:
    ns.builtin_option_name["help"] = {"--h", "--help"}
    bot_admin = on_alconna(
        Alconna(
            "admin",
            Option("-l|--list", help_text="查看 Bot管理员 列表"),
            Option("-i|--init", Args["token", str], help_text="初始化权限"),
            Subcommand(
                "add",
                Option("-a|--admin", Args["who?", int], help_text="增加 Bot管理员"),
                Option("-h|--helper", Args["who?", int], help_text="增加 Bot协助者"),
            ),
            Subcommand(
                "remove",
                Option("-a|--admin", Args["who?", int], help_text="取消 Bot管理员"),
                Option("-h|--helper", Args["who?", int], help_text="取消 Bot协助者"),
            ),
            meta=CommandMeta(
                description="Bot管理员相关指令",
                usage=__usage__,
                example="/admin -l",
                compact=True,
            ),
        ),
        priority=5,
        block=True,
        rule=to_me(),
    )


@bot_admin.assign("list")
async def list():
    admin_list = await get_admin_list()
    helper_list = await get_helper_list()

    await MessageFactory(
        f"Bot管理员列表：\n{admin_list}\nBot协助者列表：\n{[x for x in helper_list if x not in admin_list]}"
    ).send(at_sender=True)
    await bot_admin.finish()


@bot_admin.assign("init")
async def init(
    user: Annotated[UserInfo, getUserInfo()], token: Match[str] = AlconnaMatch("token")
):
    global authorize
    if token.result == authorize:
        await UserInfo.filter(user_id=user.user_id).update(permission="bot_admin")
        await MessageFactory("已成功授权 Bot管理员 权限").send(at_sender=True)
    else:
        await MessageFactory("token不对呢，返回控制台检查一下吧").send(at_sender=True)
    await bot_admin.finish()


@bot_admin.assign("add")
async def add(
    user: Annotated[UserInfo, getUserInfo()],
    admin_who: Query[int] = AlconnaQuery("add.admin.who", 0),
    helper_who: Query[int] = AlconnaQuery("add.helper.who", 0),
):
    if user.user_id not in await get_admin_list():
        await MessageFactory("权限不足，需 Bot管理员 权限").send(at_sender=True)
        await bot_admin.finish()

    if admin_who.available:
        if await UserInfo.check_user_exist(str(admin_who.result)):
            await UserInfo.filter(user_id=admin_who.result).update(
                permission="bot_admin"
            )
            await MessageFactory(f"已成功增加 Bot管理员：{admin_who.result}").send(
                at_sender=True
            )
        elif admin_who.result == 0:
            ...
        else:
            await MessageFactory(f"用户 {admin_who.result} 不存在").send(at_sender=True)
    if helper_who.available:
        if await UserInfo.check_user_exist(str(helper_who.result)):
            await UserInfo.filter(user_id=helper_who.result).update(
                permission="bot_helper"
            )
            await MessageFactory(f"已成功增加 Bot协助者：{helper_who.result}").send(
                at_sender=True
            )
        elif helper_who.result == 0:
            ...
        else:
            await MessageFactory(f"用户 {helper_who.result} 不存在").send(at_sender=True)

    await bot_admin.finish()


@bot_admin.assign("remove")
async def remove(
    user: Annotated[UserInfo, getUserInfo()],
    admin_who: Query[int] = AlconnaQuery("remove.admin.who", 0),
    helper_who: Query[int] = AlconnaQuery("remove.helper.who", 0),
):
    if user.user_id not in await get_admin_list():
        await MessageFactory("权限不足，需 Bot管理员 权限").send(at_sender=True)
        await bot_admin.finish()

    if admin_who.available:
        if await UserInfo.check_user_exist(str(admin_who.result)):
            await UserInfo.filter(user_id=admin_who.result).update(permission="USER")
            await MessageFactory(f"已取消 {admin_who.result} 的 Bot管理员 身份").send(
                at_sender=True
            )
        else:
            await MessageFactory(f"用户 {admin_who.result} 不存在").send(at_sender=True)
    elif helper_who.available:
        if await UserInfo.check_user_exist(str(helper_who.result)):
            await UserInfo.filter(user_id=helper_who.result).update(permission="USER")
            await MessageFactory(f"已取消 {helper_who.result} 的 Bot协助者 身份").send(
                at_sender=True
            )
        else:
            await MessageFactory(f"用户 {helper_who.result} 不存在").send(at_sender=True)
    else:
        await MessageFactory("参数缺失。").send(at_sender=True)
    await bot_admin.finish()


@DRIVER.on_startup
async def atuhorize_admin():
    if not await get_admin_list():
        global authorize
        authorize = random_text(20)
        logger.info("Admin", f"已自动生成授权token：{authorize}")
        logger.info("Admin", f"在任意平台发送 /admin -i {authorize} 即可获取 Bot管理员 权限")
