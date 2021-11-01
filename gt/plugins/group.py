import csv
import os, pathlib

from datetime import datetime
from pytz import timezone
from os.path import exists
from nonebot import on_command, CommandSession
from nonebot.log import logger

import config

FILE_NAME = os.path.join(config.DATA_DIR, 'group', 'current_list.txt')
TIME_ZONE = timezone('Asia/Shanghai')

# Adds the user into the waitlist. 
@on_command('group', aliases=('组队', '合作模式', '带我一个', '想打合作了'))
async def group(session: CommandSession):
    check_dir()
    dateInFile = existing_date()

    if dateInFile is None or dateInFile > current_time():
        dateInFileString = '上次啥时候忘了'
        if dateInFile is not None:
            dateInFileString = '上次时间是{}'.format(date_to_string_translator(dateInFile))
        currentTimeString = date_to_string_translator(current_time())
        await session.send('合作还没开吧, 现在时间是{}，{}'.format(currentTimeString, dateInFileString))
        return
    
    event = session.event.copy()

    # Adds the sender to the waiting list if the user is not there. 
    waitlist = waitlist_user()
    username = event['sender']['nickname']
    if username in waitlist:
        await session.send('{} 你已经在里面了，现在有{}'.format(username, waitlist))
        return 

    write_to_file(username)
    
    waitlist = waitlist_user()
    # Sends messages if there are 4 people already. 
    with open(FILE_NAME, newline='') as f:
        rows = f.read().splitlines()
    if len(rows) > 4:
        for row in rows:
            if row.startswith('date: '):
                continue
            answerMessage = '人够了！gogogo！'
        # Cleans up the file if there is enough people. 
        clean_up_file(True)
    else:
        answerMessage = '人还不够，现在有{}在等'.format(waitlist)
    
    await session.send(answerMessage)
    return

# Checks the current status. 
@on_command('查询合作', aliases=('查询合作模式', '查询组队', '当前合作', '几个人啊','现在几个人啊'))
async def search_group(session: CommandSession):
    check_dir()

    current_team = waitlist_user()
    if current_team == '':
        await session.send('现在还没人')
        return
    
    await session.send('现在有: {}'.format(current_team))

# Checks the current co-op date. If it doesn't exists, returns error messages which requires to set date. 
@on_command('合作时间', aliases=('合作开始时间','合作模式开始时间','这次合作模式'))
async def date(session: CommandSession) -> str:
    check_dir()
    inputDate = None

    # Translates the input date into datetime type.
    arg_str = session.current_arg_text.strip()
    if arg_str != '':
        logger.debug(f'Time is "{arg_str}"')
        try: 
            inputDate = string_to_date_translator(arg_str)
        except ValueError:
            await session.send('你这日期有问题啊，不是mm/dd/yyyy')
            return

    dateInFile = existing_date()

    # User input doesn't contains date, assume the user wants to check the start date. 
    if inputDate is None and dateInFile is not None:
        await session.send('合作{}开始'.format(date_to_string_translator(dateInFile)))
    elif inputDate is None and dateInFile is None:
        await session.send('俺也不知道合作啥时候开始')
    elif inputDate is not None:
        clean_up_file()
        newDate = date_to_string_translator(inputDate)
        write_to_file(newDate)
        await session.send('新的合作时间: {}'.format(newDate))
    return


# The current user who wants to be in the group list. 
def get_user_name(city: str) -> str:
    return 

# Checks if current list exists if not create it
def check_dir():
    if not os.path.isfile(FILE_NAME):
        pathlib.Path(FILE_NAME).touch()

# Translates a string into date. 
def string_to_date_translator(stringInput) -> date:
    return datetime.strptime(stringInput, '%m/%d/%Y').replace(tzinfo=TIME_ZONE)

# Translates a date into string with title. 
def date_to_string_translator(dateInput) -> str:
    newString = dateInput.strftime('%m/%d/%Y')
    return 'date: {}'.format(newString)

# Current time
def current_time():
    return datetime.now(TIME_ZONE)

# Create an empty file. 
def clean_up_file(keep_existing_date = False):
    if (not keep_existing_date):
        os.remove(FILE_NAME)
        check_dir()
        return

    tempDate = existing_date()
    if tempDate is not None:
        os.remove(FILE_NAME)
        check_dir()
        newDate = date_to_string_translator(tempDate)
        write_to_file(newDate)

# Returns the date in the file if exists. 
def existing_date():
    with open(FILE_NAME, newline='') as f:
        rows = f.read().splitlines()

    if len(rows) > 0:
        dateRange = rows[0]
        logger.debug(f"First row in current list file: {dateRange}")
        if dateRange.startswith('date: '):
            try: 
                return string_to_date_translator(dateRange[6:])
            except ValueError:
                return None 

# Returns the existing people in the file.
def waitlist_user():
    with open(FILE_NAME, newline='') as f:
        rows = f.read().splitlines()

    return ', '.join([rows[i] for i in range(1, len(rows))])

# Write contents in the csv file 
def write_to_file(content):
    with open(FILE_NAME, 'a', newline='') as f:
        f.write(content + '\n')
