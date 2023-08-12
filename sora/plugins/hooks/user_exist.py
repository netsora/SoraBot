"""
该钩子为事件预处理钩子
用来在处理事件前先判断用户是否存在
如果不存在则自动为其注册账号
"""
import os
import shutil

from nonebot import require
from nonebot.params import Depends
from nonebot.message import run_preprocessor
from nonebot.adapters.qqguild import Bot as GuildBot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.telegram.bot import Bot as TGBot
from nonebot.adapters.qqguild import MessageCreateEvent, AtMessageCreateEvent
from nonebot.adapters.qqguild.exception import AuditException
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent as V11GroupMessageEvent,
    PrivateMessageEvent as V11PrivateMessageEvent,
)
from nonebot.adapters.telegram.event import (
    GroupMessageEvent as TGroupMessageEvent,
    PrivateMessageEvent as TGPrivateMessageEvent,
)

require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory, PlatformTarget, extract_target

from sora.log import logger
from sora.config.path import TEMPLATE_PATH, DATABASE_PATH
from sora.utils.api import generate_id, random_text
from sora.database.rewards import Exp, Coin, Favor, EventReward
from sora.database.models.user import UserInfo
from sora.database.models.bind import UserBind
from sora.database.models.sign import UserSign


AllBot = V11Bot | GuildBot | TGBot
V11MessageEvent = V11GroupMessageEvent | V11PrivateMessageEvent
GuildMessageEvent = MessageCreateEvent | AtMessageCreateEvent
TGMessageEvent = TGroupMessageEvent | TGPrivateMessageEvent
AllEvent = V11MessageEvent | GuildMessageEvent | TGMessageEvent


loginEvent = EventReward(
    name="登录事件",
    description="第一次使用林汐",
    coin_reward=Coin(amount=50),
    exp_reward=Exp(amount=0),
    favor_reward=Favor(amount=0),
)


@run_preprocessor
async def doesexist(
    bot: AllBot, event: AllEvent, target: PlatformTarget = Depends(extract_target)
):
    user_id = generate_id()
    account = event.get_user_id()
    platform = bot.adapter.get_name()
    exist = await UserBind.check_account_exists(platform, account)
    if not exist:
        if isinstance(event, V11MessageEvent):
            user_name = event.sender.nickname
        elif isinstance(event, GuildMessageEvent):
            user_name = event.author.username  # type: ignore
        elif isinstance(event, TGMessageEvent):
            user_name = event.from_.username

        if await UserInfo.check_username(user_name):  # type: ignore
            user_name += random_text(2)  # type: ignore

        # 初始化信息
        await UserSign.create(user_id=user_id)
        await UserInfo.create_user(user_id, user_name)  # type: ignore
        await UserBind.create(user_id=user_id, platform=platform, account=account)  # type: ignore

        os.makedirs(f"{DATABASE_PATH}/user/{user_id}", exist_ok=True)
        source_path = f"{TEMPLATE_PATH}/setting.toml"
        save_path = f"{DATABASE_PATH}/user/{user_id}/setting.toml"

        shutil.copy(source_path, save_path)

        logger.success("注册", f"用户 {user_name}({user_id}) 账号信息初始化成功！")

        try:
            await MessageFactory(
                f"""
第一次使用林汐？\n
我们已为您注册全新的账户！\n
> 用户名：{user_name}（lv.1）\n
> ID：{user_id}\n
顺便奖励您 {loginEvent.coin_reward} 枚硬币。\n
『提示』如果您在其它平台已有账户，可发送 /bind 指令绑定！
                """
            ).send_to(target, bot)
        except AuditException:
            pass
