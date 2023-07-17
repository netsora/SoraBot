from pathlib import Path

from tortoise import Tortoise
from nonebot.log import logger

from sora.log import logger as Sogger
from sora.utils import DRIVER, scheduler
from sora.utils.user import generate_password
from sora.config.path import USER_BIND_DB_PATH, USER_INFO_DB_PATH, USER_SIGN_DB_PATH

from .models import UserBind, UserInfo, UserSign, bind, sign, user

bot_admin: list[str] = [str(s) for s in DRIVER.config.bot_admin]
bot_helper: list[str] = [str(s) for s in DRIVER.config.bot_helper]

DATABASE = {
    "connections": {
        "sora_user_info": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": USER_INFO_DB_PATH},
        },
        "sora_user_bind": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": USER_BIND_DB_PATH},
        },
        "sora_user_sign": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {"file_path": USER_SIGN_DB_PATH},
        }
        # 'memory_db': 'sqlite://:memory:'
    },
    "apps": {
        "sora_user_info": {
            "models": [user.__name__],
            "default_connection": "sora_user_info",
        },
        "sora_user_bind": {
            "models": [bind.__name__],
            "default_connection": "sora_user_bind",
        },
        "sora_user_sign": {
            "models": [sign.__name__],
            "default_connection": "sora_user_sign",
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

        for user_id in bot_admin:
            password = generate_password()
            user = await UserInfo.filter(user_id=user_id).first()
            if not user:
                await UserInfo.create(
                    user_id=user_id,
                    user_name=f"None{user_id[-2:]}",
                    password=password,
                    permission="bot_admin",
                    level=1,
                    exp=0,
                    coin=50,
                    jrrp=20,
                )
                await UserBind.update_or_create(user_id=user_id)
                await UserSign.update_or_create(user_id=user_id, total_days=0, continuous_days=0)
                Sogger.success("Bot 配置", f"已自动设置用户ID: {user_id} 为 Bot管理员。登录密码：{password}")
        for user_id in bot_helper:
            password = generate_password()
            user = await UserInfo.filter(user_id=user_id).first()
            if not user:
                await UserInfo.create(
                    user_id=user_id,
                    user_name=f"None{user_id[-2:]}",
                    password=password,
                    permission="bot_helper",
                    level=1,
                    exp=0,
                    coin=50,
                    jrrp=20,
                )
                await UserBind.update_or_create(user_id=user_id)
                await UserSign.update_or_create(user_id=user_id, total_days=0, continuous_days=0)
                Sogger.success("Bot 配置", f"已自动设置用户ID: {user_id} 为 Bot协助者。登录密码：{password}")

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
