from .._common.config import parse


def execute(confpath, today, yesterday, path):
    config = parse(confpath)
    basepath = _basepath(path, config.name)