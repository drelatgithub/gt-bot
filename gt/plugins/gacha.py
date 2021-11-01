import random

from nonebot import on_command, CommandSession

import config
import gt.utilities.chara as chara

# Pool is a dictionary: name -> weight (probability)
def create_default_pool(server, fei_factor=0.5, mei_factor=0.5, knight_male_factor=0.5, knight_female_factor=0.5, guarantee_2star=False):
    cinfo = chara.CHARA_INFO
    if server in chara.CHARA_SERVER:
        charas = chara.CHARA_SERVER[server]
        num_3 = len(cinfo[(cinfo.name.isin(charas)) & (cinfo.initstar == 3)])
        num_2 = len(cinfo[(cinfo.name.isin(charas)) & (cinfo.initstar == 2)]) - 2 # fei/mei, knight_male/knight_female
        num_1 = len(cinfo[(cinfo.name.isin(charas)) & (cinfo.initstar == 1)])

        weight_tot_3 = 0.0275
        weight_tot_2 = 0.9725 if guarantee_2star else 0.19
        weight_tot_1 = 0.0    if guarantee_2star else 0.7825

        weight_3 = weight_tot_3 / num_3
        weight_2 = weight_tot_2 / num_2
        weight_1 = weight_tot_1 / num_1

        pool = dict()
        for c in charas:
            initstar = cinfo[cinfo.name == c].initstar.values[0]
            if initstar == 3:
                pool[c] = weight_3
            elif initstar == 2:
                if c == "fei":
                    pool[c] = weight_2 * fei_factor
                elif c == "mei":
                    pool[c] = weight_2 * mei_factor
                elif c == "knight_male":
                    pool[c] = weight_2 * knight_male_factor
                elif c == "knight_female":
                    pool[c] = weight_2 * knight_female_factor
                else:
                    pool[c] = weight_2
            else:
                pool[c] = weight_1

        return pool
    else:
        raise Exception("Invalid server")


@on_command('十连', only_to_me=False)
async def gacha_10(session: CommandSession):
    res = do_gacha_10(session.event['user_id'], 'cn')
    res_str = '、'.join(res)
    await session.send(f'抽个屁啊，抽到了{res_str}')


def do_gacha_n(pool, n):
    return random.choices(
        population=list(pool.keys()),
        weights=pool.values(),
        k=n
    )

def do_gacha_10(user_id, server):
    res = []
    pool = create_default_pool(server)
    res.extend(do_gacha_n(pool, 9))
    pool = create_default_pool(server, guarantee_2star=True)
    res.extend(do_gacha_n(pool, 1))
    return res
