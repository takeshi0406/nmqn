from jinja2 import Environment, FileSystemLoader

def build(diffs):
    env = Environment(loader=FileSystemLoader('./nmqn/compare/templetes', encoding='utf8'))
    tpl = env.get_template('report.tpl.md')
    html = tpl.render({
        "title": diffs.name,
        "added": [{"url": x.url} for x in diffs.added],
        "deleted": [{"url": x.url} for x in diffs.deleted],
        "before_capture_path": "./test.png",
        "after_capture_path": "./test.png"
    })
    print(html)
    print("---------------------------:")