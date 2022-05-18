import io
import json
import os
from os import path
from pathlib import Path
import random

from nonebot.matcher import Matcher
import nonebot.adapters
from nonebot import on_command
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import Arg, CommandArg, ArgPlainText
from PIL import Image
from saucenao_api import SauceNao

from gt.utilities import resource, util
from gt.utilities.config import config
from gt.utilities import gachautil as gacha


USER_DATA_DIR = gacha.USER_DATA_DIR
USER_DATA_FILE = gacha.USER_DATA_FILE


USER_SETU_DAILY_LIMIT = 1

matcher_setu = on_command('色图', aliases={'瑟图', '不够涩', '不够色', '冲', '冲！'})


@matcher_setu.handle()
async def setu_get(matcher: Matcher, event: nonebot.adapters.Event, args: nonebot.adapters.Message=CommandArg()):
    user_id = event.get_user_id()
    user_id_str = str(user_id)
    server = 'cn'

    user_data = gacha.read_user_data()
    gacha.initialize_user_server_data(user_data, user_id, server)
    user_server_data = user_data[user_id_str][server]

    arg_str = args.extract_plain_text().strip()
    # Check if the user has used up daily limit.
    now_day = util.current_time().day
    if now_day != user_server_data['last_setu_day']:
        user_server_data['last_setu_day'] = now_day
        user_server_data['setu_count'] = 0

    if user_server_data['setu_count'] >= USER_SETU_DAILY_LIMIT:
        tosend = random.choice(['你今天不该再冲了！', '你冲的太快了，明天才能再来！'])
        gacha.save_user_data(user_data)
        await matcher_setu.finish(tosend)

    try:
        setu_content = resource.get_setu_with_tag(arg_str)
    except Exception as e:
        logger.error(e)
        await matcher_setu.finish(f'没有找到{arg_str}色图！')

    user_server_data['setu_count'] += 1

    res_img = Image.open(io.BytesIO(setu_content))
    seg_img = MessageSegment.image(util.pic2b64(res_img))


    # Write user data.
    gacha.save_user_data(user_data)

    await matcher_setu.finish(Message(seg_img))

