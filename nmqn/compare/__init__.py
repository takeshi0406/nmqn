from .._common import (config as c, path as p)


def execute(confpath, today, yesterday, path):
    config = c.parse(confpath)
    basepath = p.basepath(path, config.name)

    for devcon in config:
        for node in devcon.nodes:
            print(Reader(basepath, node, devcon))


class Reader(object):
    def __init__(self, basepath, node, deviceconfig):
        self._basepath = basepath
        self._node = node
        self._deviceconfig = deviceconfig

    @property
    def device(self):
        return self._node.device

    @property
    def basepath(self):
        return self._basepath / self._deviceconfig.device / self._node.name

    @property
    def resultpath(self):
        return self.basepath / "result.yml"

    def iter_stylesheets(self):
        for path in (self.basepath / "stylesheets").iterdir():
            with path.open("r") as f:
                yield f.read()