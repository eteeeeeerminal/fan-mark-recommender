import json
import dataclasses

@dataclasses.dataclass
class VtuberDataclass:
    name:str
    twitter_id:int
    twitter_screen_name:str
    twitter_name:str
    twitter_location:str
    twitter_profile:str
    fan_marks:list[str]
    fan_mark_names:list[str]
    fan_mark_indices:list[int] = dataclasses.field(default_factory=list[int])
    doc_vec:list[float] = dataclasses.field(default_factory=list[float])

def load_vdatas(path:str) -> list[VtuberDataclass]:
    with open(path, 'r', encoding="utf-8") as f:
        vdatas = json.load(f)
        return [VtuberDataclass(**d) for d in vdatas if d]

def save_vdatas(path:str, datas:list[VtuberDataclass]):
    datas = [dataclasses.asdict(d) for d in datas]
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(datas, f, ensure_ascii=False, indent=4)