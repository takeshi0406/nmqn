import re
import yaml
from urllib.robotparser import RobotFileParser


def parse(path):
    with open(path, "r") as f:
        config = yaml.load(f)
    return {d: Config.parse(config, d) for d in config["options"].keys()}


class Config(object):
    def __init__(self, robotsurl, options, nodes):
        self._robots = RobotsConfig(robotsurl)
        self.options = options
        self.nodes = nodes

    @classmethod
    def parse(cls, config, device):
        nodes = [Node.parse(n, device) for n in config["nodes"]]
        options = BrowserOptions.parse(config["options"], device)
        return cls(config["robots"][device], options, nodes)
        
    def allowed_all_url(self, nodes):
        for n in nodes:
            if not self._robots.can_fetch(n.url, self.options.useragent):
                raise RuntimeError("許可されていません")


class BrowserOptions(object):
    def __init__(self, useragent, viewport):
        self.useragent = useragent
        self.viewport = viewport

    @classmethod
    def parse(cls, config, device):
        c = config[device]
        return cls(c.get("useragent", None), c.get("viewport", None))


class Node(object):
    def __init__(self, name, url, childs):
        self.name = name
        self.url = url
        self.childs = childs

    @classmethod
    def parse(cls, conf, device):
        childs = [ChildNode.parse(x, device) for x in conf.get("childs", [])]
        return cls(conf["name"], conf["url"][device], childs)


class ChildNode(object):
    def __init__(self, name, url_regexp, childs):
        self._name = name
        self._url_regexp = re.compile(url_regexp)
        self._childs = childs

    @classmethod
    def parse(cls, conf, device):
        childs = [ChildNode.parse(x, device) for x in conf.get("childs", [])]
        return cls(conf["name"], conf["url_regexp"][device], childs)

    def parse_child_node(self, urls):
        """候補となるURLからノードを作る
        """
        for url in urls:
            if self._url_regexp.match(url):
                return Node(self._name, url, self._childs)
        raise ValueError(f"Url Not Found.: {urls}")


class RobotsConfig(object):
    def __init__(self, robotsurl):
        self._parser = RobotFileParser()
        self._parser.set_url(robotsurl)
        self._parser.read()

    def can_fetch(self, useragent, url):
        return self._parser.can_fetch(useragent, url)
