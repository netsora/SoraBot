from typing import List

from sora import config
from sora.log import logger
from nonebot import get_driver
from sora.database.models import UserInfo

from .scheduler import scheduler

__version__ = "1.0.0"

DRIVER = get_driver()

try:
    bot_admin: List[str] = [str(s) for s in DRIVER.config.bot_admin]
except Exception:
    bot_admin = []

if not bot_admin:
    logger.warning("Bot 配置", "请在配置文件中配置 Bot 管理员")
    exit()

try:
    NICKNAME: List = list(config.BotConfig.nickname)[0]
except Exception:
    NICKNAME: str = "林汐"
