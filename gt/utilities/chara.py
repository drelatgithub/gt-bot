import json
from os import path

import pandas
from PIL import Image

import config
import gt.utilities.resource as resource

CHARA_INFO_FILE = path.join(config.INTERNAL_DATA_DIR, 'list', 'charainfo.csv')
CHARA_INFO = pandas.read_csv(CHARA_INFO_FILE, encoding='utf-8')

# CHARA_NAME should be a dict of language -> (dict of chara_id -> chara_name), read from charaname.json
CHARA_NAME_FILE = path.join(config.INTERNAL_DATA_DIR, 'list', 'charaname.json')
with open(CHARA_NAME_FILE, 'r', encoding='utf-8') as f:
    CHARA_NAME = json.load(f)

CHARA_SERVER_FILE = path.join(config.INTERNAL_DATA_DIR, 'list', 'charaserver.json')
with open(CHARA_SERVER_FILE, 'r', encoding='utf-8') as f:
    CHARA_SERVER = json.load(f)

def get_chara_thumbnail(chara_id):
    chara_name = CHARA_NAME['cn-biliwiki'][chara_id]
    png_name = chara_name + "单个模型"
    return Image.open(resource.get_chara_png_file(png_name))

def get_chara_thumbnails(chara_ids, nres_line=5):
    ims = [get_chara_thumbnail(chara_id) for chara_id in chara_ids]

    max_width = max(im.width for im in ims)

    tot_height = 0
    for i in range(0, len(ims), nres_line):
        im_range = ims[i:i+nres_line]
        max_height = max(im.height for im in im_range)
        tot_height += max_height

    res = Image.new('RGBA', (max_width * nres_line, tot_height), (225, 0, 0, 0))
    y = 0
    for i in range(0, len(ims), nres_line):
        im_range = ims[i:i+nres_line]
        max_height = max(im.height for im in im_range)
        for j in range(len(im_range)):
            im = im_range[j]
            res.paste(im, (j * max_width, y))
        y += max_height

    return res
