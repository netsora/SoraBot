import time

from nonebot.plugin import PluginMetadata
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor
from nonebot.adapters.qqguild import Event as GuildEvent
from nonebot.adapters.onebot.v11 import Event as V11Event
from nonebot.adapters.telegram import Event as TGEvent

eventexpiry_expire: int = 30

__sora_plugin_meta__ = PluginMetadata(
    name="过期事件过滤器",
    description="自动过滤过期事件",
    usage="自动过滤过期事件",
    extra={"author": "A-kirami"},
)


@event_preprocessor
def event_expiry_handler(event: V11Event | GuildEvent | TGEvent) -> None:
    if isinstance(event, V11Event):
        event_time: int = event.time

        if time.time() - event_time > eventexpiry_expire:
            raise IgnoredException("事件已过期")
