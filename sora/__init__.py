import asyncio

from typing import Any
from pathlib import Path

from nonebot import logger, load_plugins
from tortoise.connection import ConnectionHandler

from sora import database

from sora.utils import DRIVER, __version__
from sora.utils.update import CheckUpdate

DBConfigType = dict[str, Any]


async def _init(self, db_config: "DBConfigType", create_db: bool):
    if self._db_config is None:
        self._db_config = db_config
    else:
        self._db_config.update(db_config)
    self._create_db = create_db
    await self._init_connections()


ConnectionHandler._init = _init

logo = r"""<g>
   _____                     ____        __
  / ___/____  _________ _   / __ )____  / /_
  \__ \/ __ \/ ___/ __ `/  / __  / __ \/ __/
 ___/ / /_/ / /  / /_/ /  / /_/ / /_/ / /_
/____/\____/_/   \__,_/  /_____/\____/\__/</g>"""


@DRIVER.on_startup
async def startup():
    logger.opt(colors=True).info(logo)
    await database.connect()

    logger.info(f"当前版本: {__version__}")

    logger.info("开始检查更新...")
    commit_info = await CheckUpdate.show_latest_commit_info()
    if commit_info:
        logger.info(commit_info)

    l_v, l_v_t = await CheckUpdate.show_latest_version()
    if l_v and l_v_t:
        if l_v != __version__:
            logger.warning("新版本已发布, 请更新")
            logger.warning(f"最新版本: {l_v} 更新时间: {l_v_t}")
        else:
            logger.success("当前已是最新版本！")
        await asyncio.sleep(3)

    # await PluginManager.init()
    # asyncio.ensure_future(check_resource())


DRIVER.on_shutdown(database.disconnect)


load_plugins(str(Path(__file__).parent / "plugins"))
