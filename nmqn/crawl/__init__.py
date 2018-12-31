from ._config import parse
from ._crawler import crawl_all_nodes
from pathlib import Path
from datetime import datetime as dt
import time


def execute(confpath, max_tab, path, headless):
    config_dict = parse(confpath)

    for result in crawl_all_nodes(config_dict, max_tab, _basepath(path), headless):
        print(result)


def _basepath(path):
    now = dt.now()
    date = now.strftime("%Y-%m-%d")
    unixtime = int(time.mktime(now.timetuple()))
    return Path(path) / date / str(unixtime)