"""网络工具"""

from dns import resolver
from nonebot import require
from nonebot.rule import to_me

require("nonebot_plugin_saa")
require("nonebot_plugin_alconna")
from nonebot_plugin_saa import Text
from arclet.alconna.args import Args
from arclet.alconna.core import Alconna
from arclet.alconna.typing import CommandMeta
from nonebot_plugin_alconna import on_alconna

dns = on_alconna(
    Alconna(
        "dns",
        Args["domain#域名", "url"]["rdtype?#记录名", "str", "A"],
        meta=CommandMeta(
            description="DNS 查询",
            usage="@bot /dns <域名> [记录名]",
            example="@bot /dns google.com",
            compact=True,
        ),
    ),
    rule=to_me(),
    priority=99,
    block=True,
)


async def _(domain: str, rdtype: str):
    try:
        answers = resolver.resolve(domain, rdtype)
        result = answers.rrset
        if result is None:
            return
        for answer in result:
            await Text(answer.to_text()).finish(at_sender=True)
    except resolver.NXDOMAIN:
        await Text("No DNS record found for the domain.").finish(at_sender=True)
    except resolver.NoAnswer:
        await Text("No A record found for the domain.").finish(at_sender=True)
