from nonebot import require

require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import add_global_extension
from nonebot_plugin_alconna.builtins.extensions.telegram import TelegramSlashExtension

add_global_extension(TelegramSlashExtension())
