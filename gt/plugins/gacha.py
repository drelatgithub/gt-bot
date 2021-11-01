from nonebot import on_command, CommandSession

@on_command('十连', only_to_me=False)
async def gacha_10(session: CommandSession):
    await session.send('抽个屁')
