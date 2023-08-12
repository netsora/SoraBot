import random
import string
from pathlib import Path

from nonebot.params import Depends
from nonebot.adapters.qqguild import MessageEvent as GuildMessageEvent
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from nonebot.adapters.telegram.event import MessageEvent as TGMessageEvent

from sora.config import Config
from sora.config.path import DATABASE_PATH
from sora.database import UserInfo, UserBind


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


async def get_bind_info(
    event: V11MessageEvent | GuildMessageEvent | TGMessageEvent, account=None
) -> UserBind:
    if account is not None:
        user = await UserBind.get(account=account)
    else:
        user = await UserBind.get(account=event.get_user_id())
    user_id = user.user_id
    user_info = await UserBind.filter(user_id=user_id).first()
    if user_info is None:
        raise Exception("User not found")
    return user_info


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


async def get_user_info(event, user_id: str | None = None) -> UserInfo:
    """
    获取用户信息
    :param event:
    :return: userInfo
    """
    if user_id is not None:
        user_id = user_id
    else:
        user_id = await get_user_id(event)
    user_info = await UserInfo.get(user_id=user_id)
    return user_info


def calculate_exp_threshold(level: int) -> int:
    """
    计算经验阈値
    :param level:用户当前的等级
    :return: threshold
    """
    base_exp = Config.get_config("Level", "base_exp", 150)
    cardinality = Config.get_config("Level", "cardinality", 1.2)
    threshold = round(int(base_exp * (cardinality**level)) / 10) * 10
    return threshold


def calculate_next_exp_threshold(level: int) -> int:
    """计算下一等级的经验阈值"""
    threshold = calculate_exp_threshold(level + 1)
    return threshold
