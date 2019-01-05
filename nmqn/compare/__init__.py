import yaml
from .._common import (config as c, path as p)


def execute(confpath, today, yesterday, path):
    config = c.parse(confpath)
    if not today:
        today = p.current_date(0)
    if not yesterday:
        yesterday = p.current_date(-1)
    
    m = NodeManager(path, config)
    for t, y in zip(m.iter_nodes(today), m.iter_nodes(yesterday)):
        print(t._path, y._path)


class NodeManager(object):
    def __init__(self, path, config):
        self._config = config
        self._path = path

    def iter_nodes(self, date):
        basepath = p.current_basepath(self._path, self._config.name, date)
        for devcon in self._config:
            for node in devcon.nodes:
                path = basepath / devcon.device
                yield Reader(path / node.name, devcon)
                yield from (Reader(path / c.name, devcon) for c in node.childs)


class ResultDiff(object):
    def __init__(self, today, yesterday):
        self._today = today
        self._yesterday = yesterday


class Reader(object):
    def __init__(self, path, deviceconfig):
        self._path = path
        self._deviceconfig = deviceconfig

    @property
    def device(self):
        return self._deviceconfig.device

    @property
    def results(self):
        results = []
        for path in self._path.iterdir():
            results.append(Result.load(path))
        return results


class Result(object):
    def __init__(self, config, path):
        self._config = config
        self._path = path

    @classmethod
    def load(cls, path):
        # TODO:: 存在しない場合の処理
        with (path / "result.yml").open("r") as f:
            config = yaml.load(f)
        return cls(config, path)

    def iter_stylesheets(self):
        for s in self._config["stylesheets"]:
            with (self._path / "stylesheets" / p.encode_css_name(s.split("?")[0])).open("r") as f:
                yield StyleSheetInfomation(s, f.read())


class StyleSheetInfomation(object):
    def __init__(self, url, stylesheet):
        self._url = url
        self._stylesheet = stylesheet