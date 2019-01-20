import pweave
from jinja2 import Environment, FileSystemLoader
import shutil
import os
from pathlib import Path

# TODO:: もっといい書き方があるはず
TEMPLETES = Environment(loader=FileSystemLoader('./nmqn/compare/templetes', encoding='utf8'))


class ReportBuilder(object):
    def __init__(self, basepath, name):
        self._basepath = basepath / "report" / name
        if os.path.exists(self._basepath):
            shutil.rmtree(self._basepath)
        self._basepath.mkdir(parents=True, exist_ok=True)

    def each_page(self, diffs):
        return EachPageBuilder(diffs, self._basepath)


class EachPageBuilder(object):
    def __init__(self, diffs, basepath):
        self._diffs = diffs
        self._path = basepath / diffs.device /diffs.nodename
        self._templete = TEMPLETES.get_template('report.tpl.md')

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
        mdpath = self._build_markdown("markdown.md")
        outpath = self._path / "index.html"
        pweave.weave(str(mdpath.relative_to(self._path)), output=str(outpath.absolute()),
                    doctype="pandoc2html")

    def _build_markdown(self, mdname):
        md = self._templete.render({
            "title": self._diffs.name,
            "added": [{"url": x.url} for x in self._diffs.added],
            "deleted": [{"url": x.url} for x in self._diffs.deleted],
            "before_capture_path": "./test.png",
            "after_capture_path": "./test.png"
        })
        mdpath = self._path / mdname
        with mdpath.open("w") as f:
            f.write(md)
        return mdpath