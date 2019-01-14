from jinja2 import Environment, FileSystemLoader

ENV = Environment(loader=FileSystemLoader('./nmqn/compare/templetes', encoding='utf8'))

def build(diffs):
    path = _build_markdown(diffs)
    raise RuntimeError("")
    print("---------------------------:")

def _build_markdown(diffs):
    md = ENV.get_template('report.tpl.md').render({
        "title": diffs.name,
        "added": [{"url": x.url} for x in diffs.added],
        "deleted": [{"url": x.url} for x in diffs.deleted],
        "before_capture_path": "./test.png",
        "after_capture_path": "./test.png"
    })