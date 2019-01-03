from .._common import (config as c, path as p)
from ._crawler import crawl_all_nodes
from pathlib import Path
import yaml


def execute(confpath, max_tab, path, headless):
    config = c.parse(confpath)
    basepath = p.basepath(path, config.name)

    for result in crawl_all_nodes(config, max_tab, basepath, headless):
        _save_result(basepath, result)
        _save_stylesheets(basepath, result)


def _save_stylesheets(basepath, result):
    for stylesheet in result.stylesheets:
        path = basepath / result.device / result.node.name / "stylesheets" / p.encode_css_name(stylesheet)
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