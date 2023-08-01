import os
import platform
from pathlib import Path

from nonebot.adapters.qqguild import Bot as GuildBot
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.telegram.bot import Bot as TGBot

from sora.log import logger
from sora.utils import DRIVER, NICKNAME
from sora.database.models import UserInfo


@DRIVER.on_bot_connect
async def remind(bot: V11Bot | GuildBot | TGBot):
    if str(platform.system()).lower() != "windows":
        restart = Path() / "restart.sh"
        if not restart.exists():
            with open(restart, "w", encoding="utf8") as f:
                f.write(
                    "pid=$(netstat -tunlp | grep "
                    + str(bot.config.port)
                    + " | awk '{print $7}')\n"
                    "pid=${pid%/*}\n"
                    "kill -9 $pid\n"
                    "sleep 3\n"
                    "python3 bot.py"
                )
            os.system("chmod +x ./restart.sh")
            logger.info("配置", "已自动生成 restart.sh 重启脚本，请检查脚本是否与本地指令符合..")
    is_restart_file = Path() / "is_restart"
    if is_restart_file.exists():
        if isinstance(bot, V11Bot):
            admin_list = await UserInfo.filter(permission="bot_admin").values_list(
                "user_id", "qq_id", flat=True
            )
            await bot.send_private_msg(
                user_id=int(str(admin_list[1])), message=f"{NICKNAME}重启完毕..."
            )
        # elif isinstance(bot, TGBot):
        #     await bot.get_chat
        # is_restart_file.unlink()
