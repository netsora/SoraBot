from typing import Any

from tortoise import Tortoise

from sora.log import logger
from sora.config import database_config
from sora.hook import on_startup, on_shutdown

from .models import Ban as Ban
from .models import Bind as Bind
from .models import Sign as Sign
from .models import User as User

DATABASE: dict[str, Any] = {"models": ["sora.database.models"]}


@on_startup(pre=True)
async def connect_database() -> None:
    """
    建立数据库连接
    """
    try:
        await Tortoise.init(
            db_url=database_config.url, modules=DATABASE, timezone="Asia/Shanghai"
        )
        await Tortoise.generate_schemas()
        logger.opt(colors=True).success("🗃️ [magenta]Database connected successful.[/]")

    except Exception as e:
        raise Exception("Database connection failed.") from e


def register_database(model: str):
    """
    注册数据库
    """
    models: list[str] = DATABASE["models"]
    models.append(model)


@on_shutdown
async def disconnect_database() -> None:
    """
    断开数据库连接
    """
    await Tortoise.close_connections()
    logger.opt(colors=True).success("🗃️ [magenta]Database disconnected successful.[/]")


# @scheduler.scheduled_job("cron", hour=0, minute=0, misfire_grace_time=10)
# async def daily_reset():
#     """
#     重置数据库相关设置
#     """
#     ...
