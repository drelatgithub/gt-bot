import asyncio
import base64
from collections import defaultdict
from datetime import datetime
from io import BytesIO

from PIL import Image
import pytz

TIME_ZONE = pytz.timezone('Asia/Shanghai')

# Timer copied from https://stackoverflow.com/questions/45419723/python-timer-with-asyncio-coroutine
class Timer:
    def __init__(self, timeout, callback, *cb_args):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job(*cb_args))

    async def _job(self, *cb_args):
        await asyncio.sleep(self._timeout)
        await self._callback(*cb_args)

    def cancel(self):
        self._task.cancel()

# Current time
def current_time():
    return datetime.now(TIME_ZONE)


# Copied from HoshinoBot.
def pic2b64(pic:Image) -> str:
    buf = BytesIO()
    pic.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return 'base64://' + base64_str
