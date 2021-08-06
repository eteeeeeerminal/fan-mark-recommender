import dataclasses

@dataclasses.dataclass
class VtuberDataclass:
    name:str
    twitter_id:str
    profile:str
    fan_marks:list[str]
    fan_mark_names:list[str]