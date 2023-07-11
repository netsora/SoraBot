from typing import List

from pydantic import BaseModel


class GoCQHTTPAccountList(BaseModel):
    uin: int
    password: str
    protocol: int


class WithGoCQHTTP(BaseModel):
    enabled: bool
    accounts: List[GoCQHTTPAccountList]
    download_domain: str
    download_version: str
    gocqhttp_webui_username: str
    gocqhttp_webui_password: str


class ConfigModel(BaseModel):
    ConfigVersion: str
    WithGoCQHTTP: WithGoCQHTTP


class RuntimeConfig(BaseModel):
    gocqhttp_accounts: list
    gocqhttp_download_domain: str
    gocqhttp_version: str
    gocqhttp_webui_username: str
    gocqhttp_webui_password: str
