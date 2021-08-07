import re
import os
import random

import numpy as np
import sentencepiece as spm
from gensim.models import Word2Vec

from vtuber_dataclass import VtuberDataclass, load_vdatas

sp = spm.SentencePieceProcessor(os.path.join("model", "sp", "sp.model"))
sp.Load("model/sp/sp.model")
model = Word2Vec.load(os.path.join("model", "w2v_gensim", "word2vec_tweet.model"))

regex_url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
regex_user = re.compile('@(\w){1,15}')

vdatas = load_vdatas(os.path.join("data", "vdata_long.json"))

def prepare_data(text:str) -> list[str]:
    # word2vecに入れる用に分割
    text = text.strip()
    text = re.sub(regex_url, "", text)
    text = re.sub(regex_user, "", text)
    data = [t.replace("▁", "").replace("#", "") for t in sp.EncodeAsPieces(text)]
    data = [d for d in data if d]
    return data

def cos_sim_matrix(matrix):
    d = matrix @ matrix.T
    norm = (matrix * matrix).sum(axis=1, keepdims=True) **.5
    return d / norm / norm.T

vdata = random.choice(vdatas)
text = vdata.name+vdata.twitter_location+vdata.twitter_profile
text = re.sub(f"[{''.join(vdata.fan_marks)}]", "", text)
data = prepare_data(text)

sum_vec = np.zeros(200)
for d in data:
    sum_vec += model.wv[d]

ave_vec = sum_vec / len(data)
fan_mark_vec = model.wv[vdata.fan_marks[0]]

print(f"fan_marks: {vdata.fan_marks}")
print("----")
print(text)
print("----")
print(cos_sim_matrix(np.stack([ave_vec, fan_mark_vec])))
print("----")

results = model.wv.most_similar(data)
for r in results:
    print(r[0], r[1])