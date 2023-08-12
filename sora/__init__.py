from typing import Any
from pathlib import Path

from nonebot import logger, load_plugins
from tortoise.connection import ConnectionHandler

from sora import database
from sora.utils import DRIVER

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
    # await PluginManager.init()
    # asyncio.ensure_future(check_resource())


DRIVER.on_shutdown(database.disconnect)


load_plugins(str(Path(__file__).parent / "plugins"))
