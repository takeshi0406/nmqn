from nmqn.lib import crawler
from urllib.parse import urljoin
from pathlib import Path


def crawl_all_nodes(config_dict, max_tab, path, headless):
    for device, config in config_dict.items():
        client = CrawlClient(config, max_tab, Path(path) / device, headless)
        for node, result in client.crawl_all_nodes(config.nodes):
            yield NodeResponse(
                device=device,
                node=node,
                stylesheets=result.stylesheets)


def _parse_css_urls(html):
    base_url = html.base_url
    result = []
    for elem in html.find("link[rel=stylesheet]"):
        url = elem.attrs.get("href", None)
        if url:
            result.append(urljoin(base_url, url))
    return result


class NodeResponse(object):
    def __init__(self, device, node, stylesheets):
        self.device = device
        self.node = node
        self.stylesheets = stylesheets


class CrawlClient(object):
    def __init__(self, config, max_tab, path, headless):
        self._config = config
        self._max_tab = max_tab
        self._headless = headless
        self._path = path

    def crawl_all_nodes(self, nodes):
        if not nodes:
            return

        self._config.check_robots_txt(nodes)

        childs = []
        with crawler.SyncCrawler(max_tab=self._max_tab, headless=self._headless, capture_path=self._path, options=self._config.options) as c:
            for node, result in zip(nodes, c.walk(nodes)):
                yield node, result
                childs += [x.parse_child_node(result.html.absolute_links) for x in node.childs]

        yield from self.crawl_all_nodes(childs)