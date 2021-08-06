import json
import os
import time
from dataclasses import asdict

from dotenv import load_dotenv
from twitter import *

from vtuber_dataclass import VtuberDataclass, load_vdatas, save_vdatas

# 環境変数
load_dotenv()
TOKEN=os.getenv("TOKEN")
TOKEN_SECRET=os.getenv("TOKEN_SECRET")
CONSUMER_KEY=os.getenv("CONSUMER_KEY")
CONSUMER_SECRET=os.getenv("CONSUMER_SECRET")

# 読み書きするファイル
LOAD_PATH = os.path.join("data", "vdata_long.json")
SAVE_PATH = os.path.join("data", "vdata_long.json")

vdatas = load_vdatas(LOAD_PATH)

twitter:Twitter = Twitter(
    auth=OAuth(TOKEN, TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
)

len_vdatas = len(vdatas)
for i in range(len_vdatas):
    print(f"start: {vdatas[i].name}")
    if vdatas[i].twitter_profile:
        print(f"skip: {vdatas[i].name}")
        continue

    try:
        data = twitter.users.show(
            screen_name=vdatas[i].twitter_screen_name, include_entities="description"
        )
        vdatas[i].twitter_id = data["id"]
        vdatas[i].twitter_name = data["name"]
        vdatas[i].twitter_location = data["location"]
        vdatas[i].twitter_profile = data["description"]
    except:
        print(f"something error: {vdatas[i].twitter_screen_name}")

    if i % 10 == 0 and i > 0:
        save_vdatas(SAVE_PATH, vdatas)
    time.sleep(3)

save(vdatas)
print(f"got {len(vdatas)} vdats")