import json
import os
from os import path
import requests
from urllib.parse import quote

from bs4 import BeautifulSoup
from PIL import Image

from .config import config

PNG_FILE_DIR = path.join(config.data_dir, 'cache', 'chara-png')
IMAGE_SEND_QUEUE_CACHE_DIR = path.join(config.cq_data_dir, 'data', 'cache', 'image-send-queue')
IMAGE_SEND_QUEUE_CACHE_MNT_DIR = path.join(config.cq_mnt_data_dir, 'data', 'cache', 'image-send-queue')
image_send_queue_id = 0

def find_png_in_biliwiki(filename):
    url_wiki = "https://wiki.biligame.com/gt/文件:{}.png".format(filename)
    r_wiki = requests.get(url_wiki)

    if r_wiki.status_code != 200:
        raise Exception(f"Failed to get {filename}.png download link.")

    bs_wiki = BeautifulSoup(r_wiki.text, "html.parser")
    url_png = bs_wiki.body.find('div', attrs={'class': 'fullImageLink'}).find('a')['href']
    r_png = requests.get(url_png, stream=True)

    if r_png.status_code != 200:
        raise Exception(f"Failed to download {filename}.png file.")

    return r_png.content

def get_chara_png_file(filename):
    fullname = path.join(PNG_FILE_DIR, filename + '.png')
    if not path.isfile(fullname):
        os.makedirs(PNG_FILE_DIR, exist_ok=True)
        with open(fullname, 'wb') as f:
            f.write(find_png_in_biliwiki(filename))

    return fullname

def get_rank_png_file(rank:int):
    if rank < 1 or rank > 3:
        raise Exception(f"Rank {rank} is not in range [1, 3].")

    filename = f'Rank{rank}_{rank}'
    fullname = path.join(PNG_FILE_DIR, filename + '.png')
    if not path.isfile(fullname):
        os.makedirs(PNG_FILE_DIR, exist_ok=True)
        with open(fullname, 'wb') as f:
            f.write(find_png_in_biliwiki(filename))
    return fullname

def push_image_send_queue(im):
    global image_send_queue_id
    image_name = f'{image_send_queue_id}.png'
    os.makedirs(IMAGE_SEND_QUEUE_CACHE_DIR, exist_ok=True)
    im.save(path.join(IMAGE_SEND_QUEUE_CACHE_DIR, image_name))
    image_send_queue_id += 1
    return image_name


def get_setu_with_tag(tag: str):
    tag_safe = quote(tag)
    url_loli = f'https://api.lolicon.app/setu/v2?r18=0&tag={tag_safe}&size=original&size=regular'
    r_loli = requests.get(url_loli)
    if r_loli.status_code != 200:
        raise Exception(f"Failed to get setu with tag {tag}.")
    j_loli = json.loads(r_loli.text)
    data_loli = j_loli['data']
    if len(data_loli) == 0:
        raise Exception(f"No setu with tag {tag}.")

    available_urls = data_loli[0]['urls']
    if 'regular' not in available_urls:
        raise Exception(f"No regular size setu with tag {tag}.")
    url_regular = available_urls['regular']

    r_regular = requests.get(url_regular)
    return r_regular.content
    
if __name__ == "__main__":
    quote("asdfdsf傻逼/\\rfrm")
