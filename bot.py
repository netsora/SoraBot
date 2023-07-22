import nonebot
import matcher_patch as matcher_patch
from nonebot.adapters.telegram import Adapter as TG_Adapter
from nonebot.adapters.qqguild import Adapter as QQGUILD_Adapter
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.adapters.onebot.v12 import Adapter as ONEBOT_V12Adapter

nonebot.init()

driver = nonebot.get_driver()

driver.register_adapter(ONEBOT_V11Adapter)
driver.register_adapter(ONEBOT_V12Adapter)
driver.register_adapter(QQGUILD_Adapter)
driver.register_adapter(TG_Adapter)

nonebot.load_builtin_plugins("echo")

nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugin("sora")


if __name__ == "__main__":
    nonebot.run()
