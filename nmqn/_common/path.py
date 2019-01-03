import time
from pathlib import Path
from datetime import datetime as dt
from base64 import urlsafe_b64encode

def basepath(path, name):
    now = dt.now()
    date = now.strftime("%Y-%m-%d")
    unixtime = int(time.mktime(now.timetuple()))
    return Path(path) / name / date / str(unixtime)

def encode_css_name(stylesheet):
    return urlsafe_b64encode(stylesheet.raw_url.encode("utf-8")).decode("utf-8") + ".css"