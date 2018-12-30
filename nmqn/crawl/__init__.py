from nmqn.lib import crawler
from ._config import parse

def execute(path, max_tab, headless):
    config = parse(path)

    #
    for device, config in parse(path).items():
        client = CrawlClient(config, max_tab, headless)
        for page in client.crawl_all_nodes(config.nodes):
            print(page)
        
    return

    #


class CrawlClient(object):
    def __init__(self, config, max_tab, headless):
        self._config = config
        self._max_tab = max_tab
        self._headless = headless

    def crawl_all_nodes(self, nodes):
        self._config.allowed_all_url(nodes)

        childs = []
        with crawler.SyncCrawler(max_tab=self._max_tab, headless=self._headless) as c:
            for result, node in zip(c.walk([n.url for n in nodes]), nodes):
                yield result
                childs += [c.parse_child_node(result.html.absolute_links) for c in node.childs]

        yield from self.crawl_all_nodes(childs)