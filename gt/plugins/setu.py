import io
import json
import os
from os import path
from pathlib import Path
import random

from nonebot import on_command, CommandSession
from nonebot.log import logger
from aiocqhttp import MessageSegment
from PIL import Image

import config
from gt.utilities import chara, resource, util
from gt.plugins import gacha

USER_DATA_DIR = path.join(config.DATA_DIR, 'gacha')
USER_DATA_FILE = path.join(USER_DATA_DIR, 'users.json')


SETU_ALIASES = ('涩图', '瑟图', '不够涩', '不够色')
USER_SETU_DAILY_LIMIT = 2



@on_command('色图', aliases=SETU_ALIASES, only_to_me=False)
async def setu_get(session: CommandSession):
    user_id = session.event['user_id']
    user_id_str = str(user_id)
    server = 'cn'

    user_data = gacha.read_user_data()
    gacha.initialize_user_server_data(user_data, user_id, server)
    user_server_data = user_data[user_id_str][server]

    arg_str = session.current_arg_text.strip()
    # Check if the user has used up daily limit.
    now_day = util.current_time().day
    if now_day != user_server_data['last_setu_day']:
        user_server_data['last_setu_day'] = now_day
        user_server_data['setu_count'] = 0

    if user_server_data['setu_count'] >= USER_SETU_DAILY_LIMIT:
        await session.send(random.choice(['你今天不该再冲了！', '你冲的太快了，明天才能再来！']))
        gacha.save_user_data(user_data)
        return
    else:
        user_server_data['setu_count'] += 1

    try:
        setu_content = resource.get_setu_with_tag(arg_str)
    except Exception as e:
        logger.error(e)
        await session.send(f'没有找到{arg_str}色图！')
        return

    res_img = Image.open(io.BytesIO(setu_content))
    seg_img = MessageSegment.image(util.pic2b64(res_img))


    # Write user data.
    gacha.save_user_data(user_data)

    await session.send(seg_img)

