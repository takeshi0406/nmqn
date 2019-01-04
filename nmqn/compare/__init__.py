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
        print(t._basepath, y._basepath)


class NodeManager(object):
    def __init__(self, path, config):
        self._config = config
        self._path = path

    def iter_nodes(self, date):
        basepath = p.current_basepath(self._path, self._config.name, date)
        for devcon in self._config:
            yield Reader(basepath, devcon)


class Reader(object):
    def __init__(self, basepath, deviceconfig):
        self._basepath = basepath / deviceconfig.device
        self._deviceconfig = deviceconfig

    @property
    def device(self):
        return self._deviceconfig.device

    @property
    def results(self):
        results = []
        for path in self._basepath.iterdir():
            results.append(Result.load(path))
        return results


class Result(object):
    def __init__(self, config, path):
        self._config = config
        self._path = path

    @classmethod
    def load(cls, path):
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