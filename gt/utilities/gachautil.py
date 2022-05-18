from os import path
import json

from .config import config

USER_DATA_DIR = path.join(config.data_dir, 'gacha')
USER_DATA_FILE = path.join(USER_DATA_DIR, 'users.json')

def initialize_user_server_data(data, user_id, server):
    user_id_str = str(user_id)
    if user_id_str not in data:
        data[user_id_str] = dict()
    if server not in data[user_id_str]:
        data[user_id_str][server] = dict()

    user_server_data = data[user_id_str][server]
    if 'charas' not in user_server_data:
        user_server_data['charas'] = []
    if 'crystals' not in user_server_data:
        user_server_data['crystals'] = 0
    if 'mileage' not in user_server_data:
        user_server_data['mileage'] = 0
    if 'aqi_curse' not in user_server_data:
        user_server_data['aqi_curse'] = 0

    if '10_pull_count' not in user_server_data:
        user_server_data['10_pull_count'] = 0
    if 'last_10_pull_day' not in user_server_data:
        user_server_data['last_10_pull_day'] = -1
    if '100_pull_count' not in user_server_data:
        user_server_data['100_pull_count'] = 0
    if 'last_100_pull_day' not in user_server_data:
        user_server_data['last_100_pull_day'] = -1

    if 'setu_count' not in user_server_data:
        user_server_data['setu_count'] = 0
    if 'last_setu_day' not in user_server_data:
        user_server_data['last_setu_day'] = -1

def read_user_data():
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
