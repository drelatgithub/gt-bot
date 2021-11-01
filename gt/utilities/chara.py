import json
from os import path

import pandas

import config

CHARA_INFO_FILE = path.join(config.INTERNAL_DATA_DIR, 'list', 'charainfo.csv')
CHARA_INFO = pandas.read_csv(CHARA_INFO_FILE, encoding='utf-8')

# TODO: CHARA_NAME should be a dict of language -> (dict of chara_id -> chara_name), read from charaname.json
CHARA_NAME = dict()

CHARA_SERVER_FILE = path.join(config.INTERNAL_DATA_DIR, 'list', 'charaserver.json')
with open(CHARA_SERVER_FILE, 'r', encoding='utf-8') as f:
    CHARA_SERVER = json.load(f)
