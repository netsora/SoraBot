import nonebot
import matcher_patch
from nonebot.adapters.qqguild import Adapter as QQGUILD_Adapter
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.adapters.onebot.v12 import Adapter as ONEBOT_V12Adapter

nonebot.init()

driver = nonebot.get_driver()

driver.register_adapter(ONEBOT_V11Adapter)
driver.register_adapter(QQGUILD_Adapter)
driver.register_adapter(ONEBOT_V12Adapter)

nonebot.load_builtin_plugins("echo")

nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugin("sora")


from sora import config

if config.WithGoCQHTTP.enabled:
    nonebot.load_plugin("nonebot_plugin_gocqhttp")

if __name__ == "__main__":
    nonebot.run()
