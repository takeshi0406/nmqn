import yaml
from pathlib import Path
from difflib import unified_diff
from .._common import (config as c, path as p)
from ._view import ReportBuilder


def execute(confpath, today, yesterday, path):
    config = c.parse(confpath)
    if not today:
        today = p.current_date(0)
    if not yesterday:
        yesterday = p.current_date(-1)
    
    basepath = Path(path) / config.name
    m = NodeManager(basepath, config)
    rb = ReportBuilder(basepath, f"{yesterday}-{today}")

    for t, y in zip(m.iter_nodes(today), m.iter_nodes(yesterday)):
        # 差分を取る
        diffs = AssetsDiffs.parse(t, y)
        rb.build(diffs)


class NodeManager(object):
    def __init__(self, basepath, config):
        self._config = config
        self._basepath = basepath / "logs"

    def iter_nodes(self, date):
        basepath = p.current_path(self._basepath, date)
        for devcon in self._config:
            for node in devcon.nodes:
                path = basepath / devcon.device
                yield Reader(path / node.name, devcon)
                yield from (Reader(path / c.name, devcon) for c in node.childs)


class AssetsDiffs(object):
    def __init__(self, name, today, yesterday):
        self._today = {x.id_url: x for x in today}
        self._yesterday = {x.id_url: x for x in yesterday}
        self.name = name

    @classmethod
    def parse(cls, today, yesterday):
        return cls(today.name, today.iter_stylesheets(), yesterday.iter_stylesheets())

    @property
    def added(self):
        keys = set(self._today.keys()) - set(self._yesterday.keys())
        return [self._today[k] for k in keys]

    @property
    def deleted(self):
        keys = set(self._yesterday.keys()) - set(self._today.keys())
        return [self._yesterday[k] for k in keys]

    @property
    def diffs(self):
        keys = set(self._today.keys()) & set(self._yesterday.keys())
        return [FileDiff(self._today[k], self._yesterday[k]) for k in keys]


class FileDiff(object):
    def __init__(self, today_asset, yesterday_asset):
        self._t = today_asset
        self._y = yesterday_asset
        with today_asset.path.open("r") as tf, yesterday_asset.path.open("r") as yf:
            self.diff = "".join(unified_diff(tf.readlines(), yf.readlines()))
    
    @property
    def url(self):
        return self._t.url

    @property
    def id_url(self):
        return self._t.id_url

    def is_changed(self):
        return len(self.diff) >= 1


class Reader(object):
    def __init__(self, path, deviceconfig):
        self._path = path
        self._deviceconfig = deviceconfig
    
    @property
    def name(self):
        return self._deviceconfig.name

    @property
    def device(self):
        return self._deviceconfig.device

    @property
    def result(self):
        with (self._path / "result.yml").open("r") as f:
            config = yaml.load(f)
        return config

    def iter_stylesheets(self):
        for s in self.result["stylesheets"]:
            yield StyleSheetInfomation(s["url"], self._path / "stylesheets" / s["path"])


class StyleSheetInfomation(object):
    def __init__(self, url, path):
        self.url = url
        self.path = path
    
    @property
    def id_url(self):
        # TODO:: 数字はバージョンであることが多いので塗りつぶす
        return p.identify_url(self.url)