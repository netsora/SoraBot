from typing import Union

from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot import require, on_command
from nonebot.plugin import PluginMetadata
from nonebot.internal.adapter import Message
from nonebot.params import ArgStr, CommandArg
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory
from tortoise.exceptions import DoesNotExist, ValidationError

from sora.database import UserBind, UserInfo
from sora.utils.user import generate_id, get_user_login_list

__plugin_meta__ = PluginMetadata(
    name="登录",
    description="登录您的专属账户",
    usage="/注册\n/登录",
    extra={"author": "mute.", "priority": 1},
)


register = on_command(
    cmd="注册",
    aliases={"register"},
    priority=1,
    block=True,
    rule=to_me(),
    state={
        "name": "register",
        "description": "注册 SoraBot 账号",
        "usage": "@bot /注册 [用户名] [密码]",
        "priority": 1,
    },
)
login = on_command(
    cmd="登录",
    aliases={"绑定", "login", "bind"},
    priority=1,
    block=True,
    rule=to_me(),
    state={
        "name": "login",
        "description": "登录 SoraBot 账号",
        "usage": "@bot /登录 [用户名] [密码]",
        "priority": 1,
    },
)
login_list = on_command(
    cmd="登录信息",
    aliases={"绑定信息"},
    priority=1,
    block=True,
    rule=to_me(),
    state={
        "name": "login_list",
        "description": "查询 SoraBot 绑定列表",
        "usage": "@bot /登录信息",
        "priority": 1,
    },
)


@register.handle()
async def register_user_info(state: T_State, msg: Message = CommandArg()):
    message = msg.extract_plain_text().split()

    user_id = generate_id()
    state["user_id"] = user_id

    match len(message):
        case 2:
            state["user_name"] = message[0]
            state["password"] = message[1]

        case _:
            if len(message) == 1:
                state["user_name"] = message[0]


@register.got("user_name", prompt="请输入用户名")
async def get_user_name(state: T_State, user_name: str = ArgStr("user_name")):
    state["user_name"] = user_name


@register.got("password", prompt="请输入密码")
async def get_user_password(state: T_State, password: str = ArgStr("password")):
    state["password"] = password


@register.handle()
async def register_user_info_(event: Union[V11MessageEvent, GuildMessageEvent, TGMessageEvent], state: T_State):
    user_id = state.get("user_id")
    user_name = state.get("user_name")
    password = state.get("password")

    if isinstance(event, V11MessageEvent):
        platform = "QQ"
    elif isinstance(event, TGMessageEvent):
        platform = "Telegram"
    else:
        platform = "QQ频道"

    try:
        await UserInfo.update_or_create(
            user_id=user_id,
            user_name=user_name,
            password=password,
            permission="user",
            coin=50,
            jrrp=20,
        )
        match platform:
            case "QQ":
                await UserBind.update_or_create(user_id=user_id, user_qq_id=event.get_user_id())
            case "QQ频道":
                await UserBind.update_or_create(user_id=user_id, user_qqguild_id=event.get_user_id())
            case "Telegram":
                await UserBind.update_or_create(user_id=user_id, telegram_id=event.get_user_id())
        await MessageFactory(
            f"注册成功！\n > 用户名：{user_name}\n > ID：{user_id}\n奖励您50枚硬币，好感度增加20%\n"  # noqa: E501
            f"『提示』我们已自动将 您的账户与 您的 {platform}ID 绑定。您可以通过发送 [/登录信息] 查询自己的绑定信息。"  # noqa: E501
        ).send(at_sender=True)

    except ValidationError:
        await MessageFactory("注册失败。用户名不可大于10位").send(at_sender=True)

    except DoesNotExist:
        await MessageFactory("注册失败。该用户名已被注册").send(at_sender=True)

    await register.finish()


@login.handle()
async def login_platform(state: T_State, msg: Message = CommandArg()):
    message = msg.extract_plain_text().split()

    match len(message):
        case 2:
            state["user_id"] = message[0]
            state["password"] = message[1]

        case _:
            if len(message) == 1:
                state["user_id"] = message[0]


@login.got("user_id", prompt="请输入您的ID")
async def get_user_id_(state: T_State, user_id: str = ArgStr("user_id")):
    state["user_id"] = user_id


@login.got("password", prompt="请输入密码")
async def get_user_password_(state: T_State, password: str = ArgStr("password")):
    state["password"] = password


@login.handle()
async def login_platform_(event: Union[V11MessageEvent, GuildMessageEvent, TGMessageEvent], state: T_State):
    input_user_id = state.get("user_id")
    input_password = state.get("password")

    user_info = await UserInfo.get_or_none(user_id=input_user_id).values("user_id", "password")
    user_id = user_info["user_id"]
    password = user_info["password"]

    if input_user_id != user_id or input_password != password:
        await MessageFactory("账号或密码错误，请重新输入").send(at_sender=True)
        await login.finish()

    if isinstance(event, V11MessageEvent):
        platform = "QQ"
    elif isinstance(event, GuildMessageEvent):
        platform = "QQ频道"
    else:
        platform = "Telegram"

    try:
        match platform:
            case "QQ":
                await UserBind.filter(user_id=user_id).update(user_qq_id=str(event.get_user_id()))
            case "QQ频道":
                await UserBind.filter(user_id=user_id).update(user_qqguild_id=str(event.get_user_id()))
            case "Telegram":
                await UserBind.filter(user_id=user_id).update(telegram_id=str(event.get_user_id()))
    except ValidationError:
        await MessageFactory("注册失败。用户名不可大于10位").send(at_sender=True)

    except DoesNotExist:
        await MessageFactory("注册失败。该用户名已被注册").send(at_sender=True)

    msg = f"""
    登录成功！\n > ID：{user_id}\n > 登录平台：{platform}\n提示』您可以通过发送 [/登录信息] 查询自己的绑定信息。
    """
    await MessageFactory(msg).send(at_sender=True)
    await login.finish()


@login_list.handle()
async def get_login_list(event: Union[V11MessageEvent, GuildMessageEvent, TGMessageEvent]):
    list = await get_user_login_list(event)
    msg = f"""
    您的登录信息如下：
      > QQ：{list[1] if list[1] is not None else "暂未绑定"}\n
      > QQ频道：{list[2] if list[2] is not None else "暂未绑定"}\n
      > Discord：{list[3] if list[3] is not None else "暂未绑定"}\n
      > Telegram：{list[4] if list[4] is not None else "暂未绑定"}\n
      > Bilibili：{list[5] if list[5] is not None else "暂未绑定"}\n
      > Arcaea：{list[6] if list[6] is not None else "暂未绑定"}\n
      > Phigros：{list[7] if list[7] is not None else "暂未绑定"}
    """

    await MessageFactory(msg).send(at_sender=True)
    await login_list.finish()
