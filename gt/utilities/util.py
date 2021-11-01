import base64
from collections import defaultdict
from datetime import datetime
from io import BytesIO

from PIL import Image
import pytz

# Copied from HoshinoBot.
class DailyNumberLimiter:
    tz = pytz.timezone('Asia/Shanghai')
    
    def __init__(self, max_num):
        self.today = -1
        self.count = defaultdict(int)
        self.max = max_num

    def check(self, key) -> bool:
        now = datetime.now(self.tz)
        day = now.day
        if day != self.today:
            self.today = day
            self.count.clear()
        return bool(self.count[key] < self.max)

    def get_num(self, key):
        return self.count[key]

    def increase(self, key, num=1):
        self.count[key] += num

    def reset(self, key):
        self.count[key] = 0

# Copied from HoshinoBot.
def pic2b64(pic:Image) -> str:
    buf = BytesIO()
    pic.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return 'base64://' + base64_str
