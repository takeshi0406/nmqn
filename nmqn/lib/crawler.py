from pyppeteer import launch
import asyncio
from requests_html import HTML
from pathlib import Path
from base64 import urlsafe_b64encode


class SyncCrawler(object):
    def __init__(self, *, max_tab, headless=True, capture_path=None):
        self._headless = headless
        self._max_tab = max_tab
        self._capture_path = Path(capture_path) if capture_path else None

    def __enter__(self):
        self._loop = asyncio.get_event_loop()
        return self

    def __exit__(self, *exc):
        self._loop.close()
        return False

    def walk(self, urls):
        for targets in self._each_slice(urls, self._max_tab):
            result = self._loop.run_until_complete(_async_fetch(
                targets,
                headless=self._headless,
                capture_path=self._capture_path))
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


async def _async_fetch(urls, *, headless, capture_path):
    async with AsyncCrawler(headless=headless) as c:
        async def _inner(url):
            async with await c.open(url) as page:
                resp = Response(await page.fetch())
                if capture_path is not None:
                    resp.path = await page.screenshot(capture_path.joinpath(urlsafe_b64encode(url.encode("utf-8")).decode()).with_suffix(".png"))
            return resp
        return await asyncio.gather(*[_inner(u) for u in urls])


class Response(object):
    def __init__(self, html, screenshot=None):
        self.html = html
        self.screenshot = screenshot


class AsyncCrawler(object):
    def __init__(self, *, headless):
        self._headless = headless

    async def __aenter__(self):
        self._browser = await launch(headless=self._headless)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._browser.close()
        return False

    async def open(self, url):
        return await CrawlerTab.open(self._browser, url)


class CrawlerTab(object):
    def __init__(self, page, url):
        self._page = page
        self._url = url

    @classmethod
    async def open(cls, browser, url):
        page = await browser.newPage()
        await page.goto(url)
        return cls(page, url)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._page.close()
        return False

    async def fetch(self):
        content = await self._page.evaluate('document.body.textContent', force_expr=True)
        print(content)
        return HTML(html=content, url=self._url)
    
    async def screenshot(self, path):
        await self._page.screenshot(path=str(path))
        return Path(path)