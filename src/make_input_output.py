from json import load
import os

import spacy

from vtuber_dataclass import VtuberDataclass, load_vdatas, save_vdatas
from fan_mark_dic import make_emoji_dic, load_emoji_dic, emojis_to_ids

# 読み書きするファイル
LOAD_PATH = os.path.join("data", "vdata_long.json")
SAVE_PATH = os.path.join("data", "vdata_with_variables.json")

vdatas = load_vdatas(LOAD_PATH)

def vdata_to_text(vdata:VtuberDataclass) -> str:
    text = "".join((
        vdata.twitter_name, vdata.twitter_location, vdata.twitter_profile
    ))
    # 予測対象の絵文字を削除しておく
    for e in vdata.fan_marks:
        text = text.replace(e, "")
    return text

# 説明変数とする doc vecを作る
texts = [vdata_to_text(d) for d in vdatas]
nlp = spacy.load("ja_ginza")
docs = list(nlp.pipe(texts))
doc_vecs = [d.vector.tolist() for d in docs]

# 対象の絵文字を列挙する
make_emoji_dic()
emoji_dic = load_emoji_dic()
emoji_ids = [emojis_to_ids(emoji_dic, vd.fan_marks) for vd in vdatas]

# 絵文字とdoc vecをdataclassに統合して保存
len_vdatas = len(vdatas)
for i in range(len_vdatas):
    vdatas[i].fan_mark_indices = emoji_ids[i]
    vdatas[i].doc_vec = doc_vecs[i]

save_vdatas(os.path.join("data", "vdata_with_variables.json"), vdatas)