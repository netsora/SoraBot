try:
    import ujson as json
except ImportError:
    import json
from nonebot.internal.adapter import Message

from sora.utils import PROXY


def get_message_img(data: str | Message) -> list[str]:
    """
    获取消息中所有的 图片 的链接

    :param data: event.json()
    """
    img_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "image":
                    img_list.append(msg["data"]["url"])
    else:
        for seg in data["image"]:
            img_list.append(seg.data["url"])
    return img_list


def get_message_face(data: str | Message) -> list[str]:
    """
    获取消息中所有的 face Id

    :param data: event.json()
    """
    face_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "face":
                    face_list.append(msg["data"]["id"])
    else:
        for seg in data["face"]:
            face_list.append(seg.data["id"])
    return face_list


def get_message_img_file(data: str | Message) -> list[str]:
    """
    获取消息中所有的 图片file

    :param data: event.json()
    """
    file_list = []
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            for msg in message:
                if msg["type"] == "image":
                    file_list.append(msg["data"]["file"])
    else:
        for seg in data["image"]:
            file_list.append(seg.data["file"])
    return file_list


def get_message_text(data: str | Message) -> str:
    """
    获取消息中 纯文本 的信息

    :param data: event.json()
    """
    result = ""
    if isinstance(data, str):
        event = json.loads(data)
        if data and (message := event.get("message")):
            if isinstance(message, str):
                return message.strip()
            for msg in message:
                if msg["type"] == "text":
                    result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result.strip()


def get_local_proxy() -> str | None:
    """
    获取 .env* 中设置的代理
    """
    return PROXY or None
