import base64
from collections import defaultdict
from datetime import datetime
from io import BytesIO

from PIL import Image
import pytz

TIME_ZONE = pytz.timezone('Asia/Shanghai')

# Current time
def current_time():
    return datetime.now(TIME_ZONE)


# Copied from HoshinoBot.
def pic2b64(pic:Image) -> str:
    buf = BytesIO()
    pic.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return 'base64://' + base64_str
