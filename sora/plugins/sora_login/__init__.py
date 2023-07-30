from nonebot import require
from nonebot.rule import to_me
from nonebot.params import ArgStr
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from nonebot.adapters.qqguild import Bot as GuildBot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.telegram.bot import Bot as TGBot
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from arclet.alconna.args import Args
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_saa import MessageFactory
from nonebot_plugin_alconna.adapters import Image
from tortoise.exceptions import DoesNotExist, ValidationError
from nonebot_plugin_alconna import (
    Match,
    AlconnaArg,
    AlconnaMatch,
    AlconnaMatcher,
    on_alconna,
)

from sora.config import ConfigManager
from sora.config.path import DATABASE_PATH
from sora.utils.requests import AsyncHttpx
from sora.utils.helpers import HandleCancellation
from sora.database import UserBind, UserInfo, UserSign
from sora.utils.user import generate_id, get_user_id, get_user_login_list

__sora_plugin_meta__ = PluginMetadata(
    name="登录",
    description="登录您的专属账户",
    usage="/注册\n/登录",
    extra={"author": "KomoriDev", "priority": 1},
)

CoinRewards = ConfigManager.get_config("Award")["login"][0]
JrrpRewards = ConfigManager.get_config("Award")["login"][1]
ExpRewards = ConfigManager.get_config("Award")["login"][2]

register = on_alconna(
    Alconna(
        "注册",
        Args["user_name?", str]["password?", str],
        meta=CommandMeta(
            description="注册您的林汐账户",
            usage="@bot /注册 [用户名] [密码]",
            example="@bot /注册 Komorebi xxx",
            compact=True,
        ),
    ),
    priority=1,
    block=True,
    rule=to_me(),
)
login = on_alconna(
    Alconna(
        "登录",
        Args["user_id?", str]["password?", str],
        meta=CommandMeta(
            description="登录您的林汐账户",
            usage="@bot /登录 [ID] [密码]",
            example="@bot /登录 231010 xxx",
            compact=True,
        ),
    ),
    priority=1,
    block=True,
    rule=to_me(),
)
login_list = on_alconna(
    command="登录信息",
    aliases={"绑定信息"},
    priority=1,
    block=True,
    rule=to_me(),
)
change_name = on_alconna(
    Alconna(
        "改名",
        Args["changed_name?", str],
        meta=CommandMeta(
            description="设置头像",
            usage="@bot /改名 [新用户名]",
            example="@bot /改名 Komorebi",
            compact=True,
        ),
    ),
    aliases={"修改昵称", "更改昵称", "修改用户名", "更改用户名"},
    priority=1,
    block=True,
    rule=to_me(),
)
set_avatar = on_alconna(
    Alconna(
        "设置头像",
        Args["img?", Image],
        meta=CommandMeta(
            description="设置头像",
            usage="@bot /设置头像 [图片]",
            example="@bot /设置头像",
            compact=True,
        ),
    ),
    priority=1,
    block=True,
    rule=to_me(),
)


@register.handle()
async def register_user_info(
    state: T_State,
    user_name: Match[str] = AlconnaMatch("user_name"),
    password: Match[str] = AlconnaMatch("password"),
):
    state["user_id"] = generate_id()

    if user_name.available:
        state["user_name"] = user_name.result
    if password.available:
        state["password"] = password.result


@register.got(
    "user_name", prompt="请输入用户名", parameterless=[HandleCancellation("已取消")]
)
async def get_user_name(state: T_State, user_name: str = ArgStr("user_name")):
    state["user_name"] = user_name


@register.got(
    "password", prompt="请输入密码", parameterless=[HandleCancellation("已取消")]
)
async def get_user_password(state: T_State, password: str = ArgStr("password")):
    state["password"] = password


@register.handle()
async def register_user_info_(
    event: V11MessageEvent | GuildMessageEvent | TGMessageEvent, state: T_State
):
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
            level=1,
            exp=ExpRewards,
            coin=CoinRewards,
            jrrp=JrrpRewards,
        )
    except ValidationError:
        await MessageFactory("注册失败。用户名不可大于10位").send(at_sender=True)
        await register.finish()
    except DoesNotExist:
        await MessageFactory("注册失败。该用户名已被注册").send(at_sender=True)
        await register.finish()

    try:
        match platform:
            case "QQ":
                await UserBind.update_or_create(
                    user_id=user_id, qq_id=event.get_user_id()
                )
            case "QQ频道":
                await UserBind.update_or_create(
                    user_id=user_id, qqguild_id=event.get_user_id()
                )
            case "Telegram":
                await UserBind.update_or_create(
                    user_id=user_id, telegram_id=event.get_user_id()
                )
    except DoesNotExist:
        await MessageFactory("注册失败。不可重复注册").send(at_sender=True)
        await register.finish()

    await UserSign.update_or_create(
        user_id=user_id, total_days=0, continuous_days=0
    )
    await MessageFactory(
        f"""
            注册成功\n
             > 用户名：{user_name}（Lv.1）\n
             > ID：{user_id}\n
            奖励您 {CoinRewards}枚 硬币，好感度增加 {JrrpRewards}%\n
           『提示』我们已自动将 您的账户与 您的 {platform}ID 绑定。您可以通过发送 [/登录信息] 查询自己的绑定信息。\n
           （请不要忘记 /设置头像 ！）"""
    ).send(at_sender=True)

    await register.finish()


@login.handle()
async def login_platform(
    state: T_State,
    user_id: Match[str] = AlconnaMatch("user_id"),
    password: Match[str] = AlconnaMatch("password"),
):
    if user_id.available:
        state["user_id"] = user_id.result
    if password.available:
        state["password"] = password.result


@login.got(
    "user_id", prompt="请输入您的ID", parameterless=[HandleCancellation("已取消")]
)
async def get_user_id_(state: T_State, user_id: str = ArgStr("user_id")):
    state["user_id"] = user_id


@login.got(
    "password", prompt="请输入密码", parameterless=[HandleCancellation("已取消")]
)
async def get_user_password_(
    state: T_State, password: str = ArgStr("password")
):
    state["password"] = password


@login.handle()
async def login_platform_(
    event: V11MessageEvent | GuildMessageEvent | TGMessageEvent, state: T_State
):
    input_user_id = state.get("user_id")
    input_password = state.get("password")

    user_info = await UserInfo.get_or_none(user_id=input_user_id).values(
        "user_id", "user_name", "password", "level"
    )
    if user_info is None:
        await MessageFactory("ID 不合法！").send(at_sender=True)
        await login.finish()
    user_id = user_info["user_id"]
    user_name = user_info["user_name"]
    password = user_info["password"]
    level = user_info["level"]

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
                await UserBind.filter(user_id=user_id).update(
                    qq_id=str(event.get_user_id())
                )
            case "QQ频道":
                await UserBind.filter(user_id=user_id).update(
                    qqguild_id=str(event.get_user_id())
                )
            case "Telegram":
                await UserBind.filter(user_id=user_id).update(
                    telegram_id=str(event.get_user_id())
                )
    except ValidationError:
        await MessageFactory("注册失败。用户名不可大于10位").send(at_sender=True)

    except DoesNotExist:
        await MessageFactory("注册失败。该用户名已被注册").send(at_sender=True)

    msg = f"""
    登录成功！\n
     > 用户名：{user_name}（Lv.{level}）\n
     > ID：{user_id}\n
     > 登录平台：{platform}\n
   『提示』您可以通过发送 [/登录信息] 查询自己的绑定信息。
    """
    await MessageFactory(msg).send(at_sender=True)
    await login.finish()


@login_list.handle()
async def get_login_list(
    event: V11MessageEvent | GuildMessageEvent | TGMessageEvent,
):
    user_id = await get_user_id(event)
    if user_id is None:
        await MessageFactory("该账号暂未注册林汐账户，请先发送 [/注册] ").send(at_sender=True)
        await login_list.finish()

    user_login_list = await get_user_login_list(event)

    login_info = [
        f"> QQ：{user_login_list[1] if user_login_list[1] is not None else '暂未绑定'}\n",
        f"> QQ频道：{user_login_list[2] if user_login_list[2] is not None else '暂未绑定'}\n",
        f"> Discord：{user_login_list[3] if user_login_list[3] is not None else '暂未绑定'}\n",
        f"> Telegram：{user_login_list[4] if user_login_list[4] is not None else '暂未绑定'}\n",
        f"> Bilibili：{user_login_list[5] if user_login_list[5] is not None else '暂未绑定'}\n",
        f"> Arcaea：{user_login_list[6] if user_login_list[6] is not None else '暂未绑定'}\n",
        f"> Phigros：{user_login_list[7] if user_login_list[7] is not None else '暂未绑定'}\n",
    ]

    msg = "您的登录信息如下：\n" + "\n".join(login_info)

    await MessageFactory(msg).send(at_sender=True)
    await login_list.finish()


@change_name.handle()
async def change_name_(
    state: T_State, msg: Match[str] = AlconnaMatch("changed_name")
):
    if msg.available:
        state["changed_name"] = msg.result


@change_name.got(
    "changed_name",
    prompt="请输入更改后的用户名",
    parameterless=[HandleCancellation("已取消")],
)
async def get_changed_name(
    state: T_State, changed_name: str = ArgStr("changed_name")
):
    state["changed_name"] = changed_name


@change_name.handle()
async def change_name__(
    event: V11MessageEvent | GuildMessageEvent | TGMessageEvent, state: T_State
):
    user_id = await get_user_id(event)
    if user_id is None:
        await MessageFactory("该账号暂未注册林汐账户，请先发送 [/注册] ").send(at_sender=True)
        await login_list.finish()

    changed_name = state.get("changed_name")
    await UserInfo.filter(user_id=user_id).update(user_name=changed_name)

    await MessageFactory(f"更改用户名成功！\n你现在的用户名为：{changed_name}").send(
        at_sender=True
    )
    await change_name.finish()


@set_avatar.handle()
async def set_avatar_(
    matcher: AlconnaMatcher, image: Match[Image] = AlconnaMatch("img")
):
    if image.available:
        matcher.set_path_arg("img", image.result)


@set_avatar.got_path(
    "img", prompt="请发送图片", parameterless=[HandleCancellation("已取消")]
)
async def get_avatar_img(state: T_State, image: Image = AlconnaArg("img")):
    if image.url:
        state["img"] = image.url
    else:
        state["img"] = image.id


@set_avatar.handle()
async def set_avatar__(
    bot: V11Bot | GuildBot | TGBot,
    event: V11MessageEvent | GuildMessageEvent | TGMessageEvent,
    state: T_State,
):
    user_id = await get_user_id(event)
    if user_id is None:
        await MessageFactory("该账号暂未注册林汐账户，请先发送 [/注册] ").send(at_sender=True)
        await set_avatar.finish()

    url = state.get("img")

    path = DATABASE_PATH / "user" / f"{user_id}"
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    if url:
        if isinstance(event, TGMessageEvent) and isinstance(bot, TGBot):
            try:
                await AsyncHttpx.download_telegram_file(
                    url, path / "avatar.jpg", bot
                )
                await MessageFactory("头像设置成功！").send(at_sender=True)
            except Exception:
                await MessageFactory("头像设置失败...").send(at_sender=True)
        elif isinstance(event, GuildMessageEvent):
            try:
                await AsyncHttpx.download_file(
                    f"https://{url}", path / "avatar.jpg"
                )
                await MessageFactory("头像设置成功！").send(at_sender=True)
            except Exception:
                await MessageFactory("头像设置失败...").send(at_sender=True)
        else:
            try:
                await AsyncHttpx.download_file(f"{url}", path / "avatar.jpg")
                await MessageFactory("头像设置成功！").send(at_sender=True)
            except Exception:
                await MessageFactory("头像设置失败...").send(at_sender=True)
        await set_avatar.finish()
    else:
        await MessageFactory("头像设置失败...").send(at_sender=True)
        await set_avatar.finish()
