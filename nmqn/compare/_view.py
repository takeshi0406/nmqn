import pweave
from jinja2 import Environment, FileSystemLoader

from pathlib import Path

# TODO:: もっといい書き方があるはず
TEMPLETE = Environment(loader=FileSystemLoader('./nmqn/compare/templetes', encoding='utf8')).\
    get_template('report.tpl.md')


class ReportBuilder(object):
    def __init__(self, basepath, name):
        self._basepath = basepath / "report" / name

    def build(self, diffs):
        path = self._basepath
        self._basepath.mkdir(parents=True, exist_ok=True)
        mdpath = _build_markdown(diffs, path)
        outpath = path / "output.html"
        pweave.weave(str(mdpath.absolute()), output=str(outpath.absolute()), doctype="pandoc2html")
        print('ok')
        raise


def _build_markdown(diffs, path):
    md = TEMPLETE.render({
        "title": diffs.name,
        "added": [{"url": x.url} for x in diffs.added],
        "deleted": [{"url": x.url} for x in diffs.deleted],
        "before_capture_path": "./test.png",
        "after_capture_path": "./test.png"
    })
    mdpath = path / "test.md"
    with mdpath.open("w") as f:
        f.write(md)
    return mdpath