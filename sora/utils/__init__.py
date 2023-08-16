from nonebot import get_driver
from .scheduler import scheduler as scheduler

__version__ = "v1.0.0"

DRIVER = get_driver()

PROXY = DRIVER.config.proxy


try:
    NICKNAME: list[str] = [str(s) for s in DRIVER.config.nickname]
except Exception:
    NICKNAME: list[str] = ["林汐"]
