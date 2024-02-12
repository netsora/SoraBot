import logging

from pydantic import Field, BaseSettings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sora import get_driver
from sora.log import LoguruHandler, logger


class Config(BaseSettings):
    apscheduler_autostart: bool = True
    apscheduler_log_level: int = 30
    apscheduler_config: dict = Field(
        default_factory=lambda: {"apscheduler.timezone": "Asia/Shanghai"}
    )

    class Config:
        extra = "ignore"


driver = get_driver()
global_config = driver.config
plugin_config = Config(**global_config.dict())

scheduler = AsyncIOScheduler()
scheduler.configure(plugin_config.apscheduler_config)


async def _start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.success("⏱️ <y><b>Scheduler Started</b></y>")


async def _shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.opt(colors=True).info("⏱️ <y><b>Scheduler Shutdown</b></y>")


if plugin_config.apscheduler_autostart:
    driver.on_startup(_start_scheduler)
    driver.on_shutdown(_shutdown_scheduler)

aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(plugin_config.apscheduler_log_level)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())
