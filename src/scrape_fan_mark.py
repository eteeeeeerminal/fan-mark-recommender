import os
import re
import json
import glob
import time
import asyncio
from dataclasses import asdict
from functools import partial

import requests
import emoji
from bs4 import BeautifulSoup

from .vtuber_dataclass import VtuberDataclass

V_DATA_ROOT = "https://v-data.info"
V_DATA_E_ROOT = V_DATA_ROOT + "/e/"

SAVE_ROOT = "data"
emoji_pages_root = os.path.join(SAVE_ROOT, "emoji_pages")
vtuber_pages_root = os.path.join(SAVE_ROOT, "vtuber_pages")
os.makedirs(emoji_pages_root, exist_ok=True)
os.makedirs(vtuber_pages_root, exist_ok=True)

vdata_links_path = os.path.join(SAVE_ROOT, "vdata_links.json")
vdata_dict_path = os.path.join(SAVE_ROOT, "vdata.json")

def all_emoji() -> list[str]:
    return emoji.EMOJI_UNICODE_ENGLISH.values()

def greedy_emoji(emoji_str:str) -> str:
    """
    複数の絵文字を組み合わせて1つの絵文字になる場合等に,
    一番大きな組み合わせの絵文字を返します.
    前方一致で探します
    """
    for i in range(3, 0, -1):
        if emoji_str[:i] in emoji.UNICODE_EMOJI_ENGLISH:
            return emoji_str[:i]
    return ""

def emoji_str_to_generator(emoji_str:str) -> str:
    while emoji_str:
        emoji_char = greedy_emoji(emoji_str)
        emoji_str = emoji_str.replace(emoji_char, "", 1)
        if not emoji_char:
            break
        yield emoji_char

def emoji_page_file_path(file_name:str) -> str:
    return os.path.join(emoji_pages_root, file_name)

def vtuber_pages_file_path(file_name:str) -> str:
    return os.path.join(vtuber_pages_root, file_name)

def make_emoji_page_url(emoji:str) -> str:
    """
    絵文字からURLを作成

    Args:
        emoji_code (str): URLにしたい絵文字,1文字

    Returns:
        str: v-dataで使えるURL
    """
    emoji_id = str(emoji.encode("utf-8")).replace("\\x","")
    emoji_id = re.findall(r"b'(.*)'", emoji_id)[0].upper()
    return V_DATA_E_ROOT + emoji_id

def scrape_emoji_pages():
    emoji_list = all_emoji()
    for an_emoji in emoji_list:
        print(f"start: {an_emoji}")
        save_path = emoji_page_file_path(emoji.UNICODE_EMOJI_ENGLISH[an_emoji])
        save_path = save_path.replace(":", "")

        if os.path.exists(save_path):
            print(f"skip: {an_emoji}")
            continue

        response = requests.get(make_emoji_page_url(an_emoji))
        if response.status_code != 200:
            continue

        html = response.text
        with open(save_path, 'w', encoding="utf-8") as f:
            f.write(html)

        time.sleep(1)

async def extract_vtuber_link(file_path:str) -> list[str]:
    """
    絵文字ページのhtmlを読み込んで, その中にあるVtuberページのリンクをとる

    Args:
        file_path (str): 保存したhtmlのpath

    Returns:
        list[str]: urlのリスト
    """

    with open(file_path, 'r', encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    links = [a_tag.get('href') for a_tag in soup.find_all('a')]
    link_pattern = re.compile(r"(/v/.+)")
    return list(filter(link_pattern.match, links))

async def extract_vtuber_links():
    file_list = glob.glob(os.path.join(emoji_pages_root, "*"))
    extract_jobs = [partial(extract_vtuber_link, f) for f in file_list]

    links = await asyncio.gather(*[job() for job in extract_jobs])
    links = sum(links, [])
    print(f"extract {len(links)} links")
    with open(vdata_links_path, 'w', encoding="utf-8") as f:
        json.dump(links, f)

def scrape_vtuber_pages():
    with open(vdata_links_path, 'r', encoding="utf-8") as f:
        links:list[str] = json.load(f)

    for link in links:
        print(f"start: {link}")
        save_path = vtuber_pages_file_path(link.replace("/v/", ""))

        if os.path.exists(save_path):
            print(f"skip: {link}")
            continue

        response = requests.get(V_DATA_ROOT+link)
        if response.status_code != 200:
            continue

        html = response.text
        with open(save_path, 'w', encoding="utf-8") as f:
            f.write(html)

        time.sleep(1)

async def extract_vtuber_profile(file_path:str) -> dict:
    """
    Vtuberの個別ページにある, 名前, twitter id, 推しマークを返す

    Args:
        file_name (str): 保存したhtmlのファイル

    Returns:
        dict: 得られたVtuberのデータ
    """

    with open(file_path, 'r', encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    name = soup.select_one(".leading-tight").get_text(strip=True)
    fan_marks:str = soup.select_one(".fanmark button").get("data-clipboard-text")
    fan_marks:list[str] = list(emoji_str_to_generator(fan_marks))
    fan_mark_names = [
        emoji.UNICODE_EMOJI_ENGLISH[m].replace(":", "")
        for m in fan_marks
    ]
    twitter_id = soup.select_one("p:-soup-contains(\"Twitter\") ~ p")
    if not twitter_id:
        return None
    twitter_id = twitter_id.get_text(strip=True)

    ret = VtuberDataclass(
        name, None, twitter_id, "", "", "",
        fan_marks, fan_mark_names
    )
    return asdict(ret)

async def extract_vtuber_profiles():
    file_list = glob.glob(os.path.join(vtuber_pages_root, "*"))
    extract_jobs = [partial(extract_vtuber_profile, f) for f in file_list]

    profiles = await asyncio.gather(*[job() for job in extract_jobs])
    print(f"extract {len(profiles)} profiles")
    with open(vdata_dict_path, 'w', encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)