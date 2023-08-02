import random
import string
import datetime
from pathlib import Path

from nonebot.params import Depends
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


async def get_user_id(
    event: V11MessageEvent | GuildMessageEvent | TGMessageEvent,
) -> str | None:
    """
    通过 event.userid 获取 ID

    :param event:
    :return: user_id
    """
    login_list = await get_bind_info(event)
    if login_list is None:
        user_id = None
    else:
        user_id = login_list.user_id

    return user_id


def get_user_avatar(user_id: str) -> Path | None:
    """
    获取用户头像
    :param event:
    :param user_id: ID
    :return: avatar_path or None
    """
    avatar_path = DATABASE_PATH / "user" / user_id / "avatar.jpg"
    if avatar_path.exists():
        return avatar_path
    return None


def getUserInfo():
    """
    获取用户信息

    get_user_info 的依赖注入版本
    :param user_id:
    :return: userInfo
    """

    async def dependency(
        event: V11MessageEvent | GuildMessageEvent | TGMessageEvent,
    ) -> UserInfo | None:
        return await get_user_info(event)

    return Depends(dependency)


async def get_user_info(event) -> UserInfo | None:
    """
    获取用户信息
    :param event:
    :return: userInfo
    """
    user_id = await get_user_id(event)
    user_info = await UserInfo.get_or_none(user_id=user_id)
    return user_info


async def get_bind_info(event) -> UserBind | None:
    """
    获取用户绑定信息
    :param user_id:
    :return: userBind
    """
    if isinstance(event, V11MessageEvent):
        user_bind = await UserBind.get_or_none(qq_id=event.get_user_id())
    elif isinstance(event, GuildMessageEvent):
        user_bind = await UserBind.get_or_none(qqguild_id=event.get_user_id())
    elif isinstance(event, TGMessageEvent):
        user_bind = await UserBind.get_or_none(telegram_id=event.get_user_id())
    else:
        user_bind = None
    return user_bind


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
