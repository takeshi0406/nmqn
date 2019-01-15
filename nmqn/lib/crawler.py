from pyppeteer import launch
import asyncio
import aiohttp
from requests_html import HTML
from pathlib import Path


class SyncCrawler(object):
    def __init__(self, *, max_tab, headless=True, capture_path=None, options=None):
        self._headless = headless
        self._max_tab = max_tab
        self._capture_path = Path(capture_path) if capture_path else None
        self._options = options

    def __enter__(self):
        self._loop = asyncio.new_event_loop()
        self._capture_path.mkdir(exist_ok=True, parents=True)
        return self

    def __exit__(self, *exc):
        self._loop.close()
        return False

    def walk(self, nodes):
        for targets in self._each_slice(nodes, self._max_tab):
            result = self._loop.run_until_complete(_async_fetch(
                targets,
                headless=self._headless,
                capture_path=self._capture_path,
                options=self._options))
            yield from result

    @staticmethod
    def _each_slice(iterable, n):
        res = []
        for x in iterable:
            res.append(x)
            if len(res) >= n:
                yield res.copy()
                res.clear()
        if res:
            yield res


async def _async_fetch(nodes, *, headless, capture_path, options):
    async with AsyncCrawler(headless=headless, options=options) as c:
        async def _inner(node):
            async with await c.open(node.url) as page:
                resp = Response(
                    await page.fetch(),
                    await page.fetchStyleSheets())
                if capture_path is not None:
                    resp.screenshot = await page.screenshot(
                        capture_path / node.name / "capture.png")
            return resp
        return await asyncio.gather(*[_inner(u) for u in nodes])


class Response(object):
    def __init__(self, html, stylesheets=None, screenshot=None):
        self.html = html
        self.stylesheets = stylesheets
        self.screenshot = screenshot


class AsyncCrawler(object):
    def __init__(self, *, headless, options):
        self._headless = headless
        self._options = options

    async def __aenter__(self):
        # CORSを無効化して、別ドメインのCSSを参照できるようにする
        # self._browser = await launch(headless=self._headless, args=['--disable-web-security'])
        self._browser = await launch(headless=self._headless)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._browser.close()
        return False

    async def open(self, url):
        return await CrawlerTab.open(self._browser, url, self._options)


class CrawlerTab(object):
    def __init__(self, page, url):
        self._page = page
        self._url = url

    @classmethod
    async def open(cls, browser, url, options):
        page = await browser.newPage()
        if options.useragent:
            await page.setUserAgent(userAgent=options.useragent)
        if options.viewport:
            await page.setViewport(viewport=options.viewport)
        await page.goto(url) #TODO:: timeout= ?
        # TODO:: wait until loaded
        return cls(page, url)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._page.close()
        return False

    async def fetch(self):
        content = await self._page.evaluate('document.documentElement.innerHTML', force_expr=True)
        url = await self._page.evaluate('window.location.href', force_expr=True)
        return HTML(html=content, url=url)
    
    async def screenshot(self, path):
        path.parent.mkdir(exist_ok=True, parents=True)
        await self._page.screenshot(path=str(path), fullPage=True)
        return Path(path)

    async def fetchStyleSheets(self):
        urls = await self._page.evaluate("""() => {
            const result = [];
            for (const s of document.styleSheets) {
                if (s.href) result.push(s.href);
            }
            return result;
        }""")
        return [await CssResponse.fetch(u) for u in urls]


class CssResponse(object):
    def __init__(self, url, css):
        self.url = url
        self.text = css

    @classmethod
    async def fetch(cls, url):
        # TODO:: ブラウザから取得したい
        async with aiohttp.request('GET', url) as response:
            css = await response.text()
        return cls(url, css)