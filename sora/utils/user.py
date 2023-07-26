import random
import string
import datetime
from pathlib import Path

from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

from sora.config import ConfigManager
from sora.config.path import DATABASE_PATH
from sora.database.models import UserBind, UserInfo


def generate_id():
    """生成用户ID"""
    current_time = datetime.datetime.now().strftime("%Y%m%d")  # 获取当前日期
    random_number = random.randint(10, 99)  # 生成一个随机数
    if random_number < 10:
        random_number = "0" + str(random_number)
    user_id: str = f"{current_time}{random_number}"  # 结合日期和随机数生成ID
    return user_id


def generate_password(length=10, chars=string.ascii_letters + string.digits):
    """生成用户密码"""

    return "".join([random.choice(chars) for i in range(length)])


async def get_user_name(user_id: str) -> str:
    """
    通过 用户ID 获取 用户名

    :param event:
    :return: user_name

    """

    user_info = await UserInfo.get(user_id=user_id)
    user_name = user_info.user_name
    return user_name


async def get_user_id(event: V11MessageEvent | GuildMessageEvent | TGMessageEvent) -> str | None:
    """
    通过 平台ID 获取 用户ID

    :param event:
    :return: user_id

    已支持的平台:

    * onebot_v11
    * qqguild
    * telegram
    """
    login_list = await get_user_login_list(event)
    if login_list is None:
        user_id = None
    else:
        user_id = login_list[0]

    return str(user_id)


def get_user_avatar(user_id: str) -> Path:
    """
    获取用户头像
    :param event:
    :param user_id: ID
    :return: avatar_path
    """
    avatar_path = DATABASE_PATH / "user" / user_id / "avatar.jpg"
    return avatar_path


async def get_user_login_list(event):
    """
    通过用户ID获取登录信息
    :param event:
    :return: login_list
    """
    platforms = {
        V11MessageEvent: {"event_user_id": event.get_user_id(), "platform_id": "qq_id"},
        GuildMessageEvent: {"event_user_id": event.get_user_id(), "platform_id": "qqguild_id"},
        TGMessageEvent: {"event_user_id": event.get_user_id(), "platform_id": "telegram_id"},
    }

    platform = next((p for p in platforms.keys() if isinstance(event, p)), None)
    if not platform:
        return []

    login_list = await UserBind.get_or_none(
        **{platforms[platform]["platform_id"]: platforms[platform]["event_user_id"]}
    ).values_list(
        "user_id",
        "qq_id",
        "qqguild_id",
        "discord_id",
        "telegram_id",
        "bilibili_id",
        "arcaea_id",
        "phigros_id",
    )

    return login_list


async def get_user_coin(user_id: str) -> int:
    """
    获取用户硬币
    :param user_id:
    :return: coin
    """
    user_info = await UserInfo.get(user_id=user_id)
    coin = user_info.coin
    return coin


async def get_user_level(user_id: str) -> int:
    """
    获取用户等级
    :param user_id:
    :return: user_level
    """
    user_info = await UserInfo.get(user_id=user_id)
    user_level = user_info.level
    return user_level


async def get_user_exp(user_id: str) -> int:
    """
    获取用户经验
    :param user_id:
    :return: user_exp
    """
    user_info = await UserInfo.get(user_id=user_id)
    user_exp = user_info.exp
    return user_exp


def calculate_exp_threshold(level: int) -> int:
    """
    计算经验阈値
    :param level:用户当前的等级
    :return: threshold
    """
    base_exp = ConfigManager.get_config("Level")["base_exp"]
    cardinality = ConfigManager.get_config("Level")["cardinality"]
    threshold = round(int(base_exp * (cardinality**level)) / 10) * 10
    return threshold


def calculate_next_exp_threshold(level: int) -> int:
    """计算下一等级的经验阈值"""
    threshold = calculate_exp_threshold(level + 1)
    return threshold
