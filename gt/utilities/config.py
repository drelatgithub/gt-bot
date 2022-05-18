from pydantic import BaseModel, Extra
from nonebot import get_driver

class Config(BaseModel, extra=Extra.ignore):
    data_dir: str
    internal_data_dir: str
    cq_data_dir: str
    cq_mnt_data_dir: str

config = Config.parse_obj(get_driver().config)
