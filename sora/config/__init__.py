import platform

from .path import SORA_CONFIG
from .utils import ConfigsManager

if platform.system() == "Linux":
    import os

    hostip = (
        os.popen("cat /etc/resolv.conf | grep nameserver | awk '{ print $2 }'")
        .read()
        .replace("\n", "")
    )

Config = ConfigsManager(SORA_CONFIG)
