import pweave
from jinja2 import Environment, FileSystemLoader
import shutil
import os
from pathlib import Path

# TODO:: もっといい書き方があるはず
TEMPLETE = Environment(loader=FileSystemLoader('./nmqn/compare/templetes', encoding='utf8')).\
    get_template('report.tpl.md')


class ReportBuilder(object):
    def __init__(self, basepath, name):
        self._basepath = basepath / "report" / name
        if os.path.exists(self._basepath):
            shutil.rmtree(self._basepath)

    def each_page(self, diffs):
        return EachPageBuilder(diffs, self._basepath)


class EachPageBuilder(object):
    def __init__(self, diffs, basepath):
        self._diffs = diffs
        self._path = basepath / diffs.device /diffs.nodename

    def __enter__(self):
        self._path.mkdir(parents=True, exist_ok=True)
        self._prev_path = os.getcwd()
        os.chdir(self._path)
        return self
    
    def __exit__(self, *args):
        os.chdir(self._prev_path)
        del self._prev_path
        return False

    def build(self):
        mdpath = _build_markdown(self._diffs, self._path)
        outpath = self._path / "index.html"
        pweave.weave(str(mdpath.relative_to(self._path)), output=str(outpath.absolute()),
                    doctype="pandoc2html")


def _build_markdown(diffs, path):
    md = TEMPLETE.render({
        "title": diffs.name,
        "added": [{"url": x.url} for x in diffs.added],
        "deleted": [{"url": x.url} for x in diffs.deleted],
        "before_capture_path": "./test.png",
        "after_capture_path": "./test.png"
    })
    mdpath = path / "markdown.md"
    with mdpath.open("w") as f:
        f.write(md)
    return mdpath