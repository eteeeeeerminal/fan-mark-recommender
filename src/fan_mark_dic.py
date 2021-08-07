import os
import glob

import emoji

LOAD_PATH = os.path.join("data", "emoji_pages")
SAVE_PATH = os.path.join("data", "emoji_dic.txt")

def make_emoji_dic():
    # emoji_pagesを全部読み込んで, それを元に絵文字dicファイルを作る
    file_name_list = glob.glob(os.path.join(LOAD_PATH, "*"))
    file_name_list = [os.path.basename(p) for p in file_name_list]
    emoji_list = [emoji.EMOJI_UNICODE_ENGLISH[f":{n}:"] for n in file_name_list]
    with open(SAVE_PATH, 'w', encoding="utf-8") as f:
        f.write("\n".join(emoji_list))

def load_emoji_dic() -> dict[str, int]:
    with open(SAVE_PATH, 'r', encoding="utf-8") as f:
        emoji_list = f.read().split("\n")
    return {e:i+1 for i, e in enumerate(emoji_list)}

def emojis_to_ids(emoji_dic:dict[str, int], emojis:list[str]) -> list[int]:
    ids = [emoji_dic[e] for e in emojis]
    ids = ids + [0] * (3 - len(ids))
    return ids