import re
import yaml
from urllib.robotparser import RobotFileParser


def parse(path):
    with open(path, "r") as f:
        config = yaml.load(f)
    return {d: Config.parse(config, d) for d in config["devices"].keys()}


class Config(object):
    def __init__(self, robotsurl, useragent, nodes):
        self._robots = RobotsConfig(robotsurl)
        self._useragent = useragent
        self.nodes = nodes

    @classmethod
    def parse(cls, config, device):
        nodes = [Node.parse(n, device) for n in config["nodes"]]
        return cls(config["robots"][device], config["devices"][device], nodes)
        
    def allowed_all_url(self, nodes):
        for n in nodes:
            if not self._robots.can_fetch(n.url, self._useragent):
                raise RuntimeError("許可されていません")


class Node(object):
    def __init__(self, name, url, childs):
        self._name = name
        self._url = url
        self.childs = childs

    @classmethod
    def parse(cls, conf, device):
        childs = [ChildNode.parse(x, device) for x in conf.get("childs", [])]
        return cls(conf["name"], conf["url"][device], childs)
    
    @property
    def url(self):
        return self._url

class ChildNode(object):
    def __init__(self, name, url_regexp, childs):
        self._name = name
        self._url_regexp = re.compile(url_regexp)
        self._childs = childs

    @classmethod
    def parse(cls, conf, device):
        # TODO:: urlのコンパイル
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
