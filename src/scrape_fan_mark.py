import os
import re

V_DATA_E_ROOT = "https://v-data.info/e/"

def make_emoji_page_url(emoji:str) -> str:
    """
    絵文字からURLを作成

    Args:
        emoji_code (str): URLにしたい絵文字,1文字

    Returns:
        str: v-dataで使えるURL
    """
    assert len(emoji) == 1
    emoji_id = str(emoji.encode("utf-8")).replace("\\x","")
    emoji_id = re.findall(r"b'(.*)'", emoji_id)[0].upper()
    return V_DATA_E_ROOT + emoji_id

