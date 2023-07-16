from typing import List, Optional

from pydantic import BaseModel


class GoCQHTTPAccountList(BaseModel):
    uin: int
    password: str
    protocol: int


class WithGoCQHTTP(BaseModel):
    enabled: bool
    accounts: Optional[List[GoCQHTTPAccountList]]
    download_domain: str
    download_version: str
    gocqhttp_webui_username: str
    gocqhttp_webui_password: str


class ConfigModel(BaseModel):
    ConfigVersion: str
    WithGoCQHTTP: WithGoCQHTTP


class RuntimeConfig(BaseModel):
    gocqhttp_accounts: Optional[list]
    gocqhttp_download_domain: str
    gocqhttp_version: str
    gocqhttp_webui_username: str
    gocqhttp_webui_password: str
