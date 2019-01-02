from ._config import parse
from ._crawler import crawl_all_nodes
from pathlib import Path
from datetime import datetime as dt
import time
from base64 import urlsafe_b64encode
import yaml


def execute(confpath, max_tab, path, headless):
    config = parse(confpath)
    basepath = _basepath(path, config.name)

    for result in crawl_all_nodes(config, max_tab, basepath, headless):
        _save_result(basepath, result)
        _save_stylesheets(basepath, result)


def _basepath(path, name):
    now = dt.now()
    date = now.strftime("%Y-%m-%d")
    unixtime = int(time.mktime(now.timetuple()))
    return Path(path) / name / date / str(unixtime)


def _save_stylesheets(basepath, result):
    for stylesheet in result.stylesheets:
        path = basepath / result.device / result.node.name / "stylesheets" / _encode_css_name(stylesheet)
        path.parent.mkdir(exist_ok=True, parents=True)
        with path.open("w") as f:
            f.write(stylesheet.text)


def _save_result(basepath, result):
    path = basepath /result.device / result.node.name / "result.yml"
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open("w") as f:
        f.write(yaml.dump({
            "name": result.node.name,
            "url": result.node.url,
            "redirected": result.html.url,
            "stylesheets": [s.url for s in result.stylesheets]
            }, default_flow_style=False))


def _encode_css_name(stylesheet):
    return urlsafe_b64encode(stylesheet.raw_url.encode("utf-8")).decode("utf-8") + ".css"

