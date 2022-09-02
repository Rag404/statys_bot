import os
from discord import Bot, Embed, Message
from data.bot_config import OWNER_ID
from datetime import datetime
from importlib import import_module

def log(*args) -> None:
    text = ' '.join(map(str, args))
    return print(datetime.now().strftime('%d/%m %H:%M'), "-", text)


async def send_to_owner(client: Bot, text: str, thumbnailURL: str=None) -> Message:
    owner = client.get_user(OWNER_ID)
    embed = Embed(title="🔔 Notification", description=text)
    if thumbnailURL: embed.set_thumbnail(url=thumbnailURL)
    return await owner.send(embed=embed)


def get_locales(category: str, *path):
    locales = {}
    for filename in os.listdir("locales"):
        if os.path("locales/" + filename) and filename.endswith(".py"):
            value = import_module(f"locales.{filename[:3]}.{category}")
            for i in path:
                value = value[i]
            locales[filename[:3]] = value