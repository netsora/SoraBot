from pathlib import Path

from tortoise import Tortoise
from nonebot.log import logger

from sora.utils import scheduler
from sora.config.path import (
    USER_BAN_DB_PATH,
    USER_BIND_DB_PATH,
    USER_INFO_DB_PATH,
    USER_SIGN_DB_PATH,
)

from .models import BanUser as BanUser
from .models import UserBind as UserBind
from .models import UserInfo as UserInfo
from .models import UserSign as UserSign
from .models import ban, bind, sign, user


DATABASE = {
    "connections": {
        "ban_info": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": USER_BAN_DB_PATH},
        },
        "user_info": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": USER_INFO_DB_PATH},
        },
        "user_bind": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": USER_BIND_DB_PATH},
        },
        "user_sign": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": USER_SIGN_DB_PATH},
        },
        # 'memory_db': 'sqlite://:memory:'
    },
    "apps": {
        "ban_info": {
            "models": [ban.__name__],
            "default_connection": "ban_info",
        },
        "user_info": {
            "models": [user.__name__],
            "default_connection": "user_info",
        },
        "user_bind": {
            "models": [bind.__name__],
            "default_connection": "user_bind",
        },
        "user_sign": {
            "models": [sign.__name__],
            "default_connection": "user_sign",
        },
        # 'memory_db':            {
        #     'models':             [memory_db.__name__],
        #     'default_connection': 'memory_db',
        # }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}


def register_database(db_name: str, models: str, db_path: str | Path | None):
    """
    注册数据库
    """
    if db_name in DATABASE["connections"] and db_name in DATABASE["apps"]:
        DATABASE["apps"][db_name]["models"].append(models)
    else:
        DATABASE["connections"][db_name] = {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": db_path},
        }
        DATABASE["apps"][db_name] = {
            "models": [models],
            "default_connection": db_name,
        }


async def connect():
    """
    建立数据库连接
    """
    try:
        await Tortoise.init(DATABASE)
        await Tortoise.generate_schemas()
        logger.opt(colors=True).success("<u><y>[数据库]</y></u><g>连接成功</g>")

    except Exception as e:
        logger.opt(colors=True).warning(f"<u><y>[数据库]</y></u><r>连接失败:{e}</r>")
        raise e


async def disconnect():
    """
    断开数据库连接
    """
    await Tortoise.close_connections()
    logger.opt(colors=True).success("<u><y>[数据库]</y></u><r>连接已断开</r>")


@scheduler.scheduled_job("cron", hour=0, minute=0, misfire_grace_time=10)
async def daily_reset():
    """
    重置数据库相关设置
    """
    ...
