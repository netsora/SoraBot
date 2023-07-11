import random
import string
import datetime
from typing import Union

from sora.database.models import UserBind
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent


def generate_id():
    """生成用户ID"""
    current_time = datetime.datetime.now().strftime("%Y%m%d")  # 获取当前日期和时间，格式为年月日时分秒
    random_number = random.randint(10, 99)  # 生成一个随机数
    if random_number < 10:
        random_number = "0" + str(random_number)
    user_id: str = f"{current_time}{random_number}"  # 结合日期和随机数生成ID
    return user_id


def generate_password(length=10, chars=string.ascii_letters + string.digits):
    """生成用户密码"""

    return "".join([random.choice(chars) for i in range(length)])


async def get_user_id(event: Union[V11MessageEvent, GuildMessageEvent]):
    """
    通过 平台ID 获取 用户ID

    :param event:
    :return: user_id

    已支持的平台:

    * onebot_v11
    * qqguild
    """
    event_user_id = event.get_user_id()
    if isinstance(event, V11MessageEvent):
        user_bind_info = await UserBind.get_or_none(
            user_qq_id=event_user_id
        ).values_list(
            "user_id",
            "user_qq_id",
            "user_qqguild_id",
            "discord_id",
            "bilibili_id",
            "arcaea_id",
            "phigros_id",
        )
    elif isinstance(event, GuildMessageEvent):
        user_bind_info = await UserBind.get_or_none(
            user_qqguild_id=event_user_id
        ).values_list(
            "user_id",
            "user_qq_id",
            "user_qqguild_id",
            "discord_id",
            "bilibili_id",
            "arcaea_id",
            "phigros_id",
        )
    user_id = user_bind_info[0]

    return user_id
