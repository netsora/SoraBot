import pandas as pd

from nonebot import require
from nonebot.rule import to_me
from nonebot.internal.adapter.bot import Bot
from nonebot.internal.adapter.event import Event

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.args import Args
from arclet.alconna.core import Alconna
from arclet.alconna.base import Option
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import Match, on_alconna, AlconnaMatch
from nonebot_plugin_alconna.adapters import At
from nonebot_plugin_saa import MessageFactory

from sora.utils.api import random_text
from sora.utils.annotated import UserInfo
from sora.database.models.bind import UserBind
from sora.utils.user import get_user_info
from sora.utils.utils import get_setting_path

from .utils import read_value
from .model import token_manager, validate_token

__usage__ = """
绑定：@bot /绑定 <token>
获取token：@bot /绑定 -t [自定义token]
取消绑定：@bot /绑定 -r
绑定列表：@bot /绑定 -l

（指令别名：/bind）
（注：所有 token 均为 一次性token，使用过后需重新生成）
"""

__example__ = """
假如您希望在QQ频道绑定群聊中的账号数据，则您应该在群聊中输入
> 用户：@bot /绑定 -t [可以在此处自定义 token]
> Bot：已为您生成一次性token：123456

然后，您需要复制此token，来到QQ频道
> 用户：@bot /绑定 123456
> Bot：绑定成功
"""

bind = on_alconna(
    Alconna(
        "绑定",
        Args["input_token?", str],
        Option("-t|--token", Args["token?", str], help_text="生成token"),
        Option("-l|--list", Args["who?", At], alias={"列表", "信息"}, help_text="查询绑定信息"),
        Option("-r|--rebind", alias={"取消"}, help_text="取消绑定"),
        meta=CommandMeta(
            description="绑定",
            usage=__usage__,
            example=__example__,
            compact=True,
        ),
    ),
    aliases={"bind"},
    priority=5,
    block=True,
    rule=to_me(),
)


@bind.assign("$main")
async def bind_(
    bot: Bot,
    event: Event,
    userInfo: UserInfo,
    input_token: Match[str] = AlconnaMatch("input_token"),
):
    if input_token.available:
        validation_result = validate_token(input_token.result)
        if validation_result.is_valid and validation_result.user_id is not None:
            await UserBind.bind(
                validation_result.user_id,
                platform=bot.type,
                account=event.get_user_id(),
            )
            bindUserInfo = await get_user_info(event, validation_result.user_id)
            await MessageFactory(
                f"""
                绑定成功\n
                已将 {userInfo.user_name}({userInfo.user_id}) 与 {bindUserInfo.user_name}({bindUserInfo.user_id}) 绑定
                """
            ).send(at_sender=True)
        else:
            await MessageFactory("绑定失败，密钥错误！").send(at_sender=True)
    else:
        await MessageFactory("格式错误。输入 /help 绑定 查看其详细用法").send(at_sender=True)
    token_manager.remove_token(validation_result.user_id)  # type: ignore

    await bind.finish()


@bind.assign("token")
async def token_(
    user: UserInfo,
    token: Match[str] = AlconnaMatch("token"),
):
    if token.available:
        if token.result == "random":
            random_token = random_text(15, prefix="Sora/")
            token_manager.add_token(user_id=user.user_id, token=random_token)
            await MessageFactory(f"已为您生成一次性token：{random_token}").send(at_sender=True)
        else:
            token_manager.add_token(user_id=user.user_id, token=token.result)
            await MessageFactory(f"一次性token设置成功：{token.result}").send(at_sender=True)
    else:
        random_token = random_text(15, prefix="Sora/")
        token_manager.add_token(user_id=user.user_id, token=random_token)
        await MessageFactory(f"已为您生成一次性token：{random_token}\n").send(at_sender=True)
    await bind.finish()


@bind.assign("list")
async def bind_list_(
    event: Event,
    who: Match[At] = AlconnaMatch("who"),
):
    if who.available:
        path = get_setting_path(who.result.target)
        show_bindinfo = await read_value(path, module="setting", key="show_bindinfo")
        if show_bindinfo:
            bindInfo = await UserBind.get_bind_info(account=who.result.target)
            df = pd.DataFrame(bindInfo)
            await MessageFactory(df.to_string(index=False)).send(at_sender=True)
        else:
            await MessageFactory("该用户已设置 “不允许查看绑定资料”").send(at_sender=True)
        await bind.finish()

    bindInfo = await UserBind.get_bind_info(event.get_user_id())
    df = pd.DataFrame(bindInfo)
    await MessageFactory(df.to_string(index=False)).send(at_sender=True)
    await bind.finish()


@bind.assign("rebind")
async def rebind(
    bot: Bot,
    userInfo: UserInfo,
):
    await UserBind.rebind(userInfo.user_id, bot.type)
    await MessageFactory("已取消绑定").send(at_sender=True)
    await bind.finish()
