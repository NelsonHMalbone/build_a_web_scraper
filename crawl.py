from urllib.parse import urlsplit,urljoin

import aiohttp
import requests
import asyncio

from aiohttp.hdrs import CONTENT_TYPE
from bs4 import BeautifulSoup, Tag

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    soup_find_h1 = soup.find("h1")
    soup_find_h2 = soup.find("h2")

    if isinstance(soup_find_h1, Tag):
        return soup_find_h1.get_text(strip=True)
    elif isinstance(soup_find_h2, Tag):
        return soup_find_h2.get_text(strip=True)
    else:
        return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    soup_find_p = soup.find("main")

    if isinstance(soup_find_p, Tag):
        return soup_find_p.get_text(strip=True)
    else:
        return ""

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    soup_find_a = soup.find_all("a")
    soup_find_a_list = []


    for x in soup_find_a:
        soup_find_a_get = x.get("href")
        soup_find_a_get_urljoin = urljoin(base_url, soup_find_a_get)
        soup_find_a_list.append(soup_find_a_get_urljoin)
    return soup_find_a_list

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    soup_find_img = soup.find_all("img")
    soup_find_img_list = []

    for i in soup_find_img:
            soup_find_img_get = i.get("src")
            if soup_find_img_get:
                soup_find_img_get_urljoin = urljoin(base_url, soup_find_img_get)
                soup_find_img_list.append(soup_find_img_get_urljoin)
            else:
                continue
    return soup_find_img_list


def normalize_url(url):
    parsed =urlsplit(url)
    netloc_parsed = parsed.netloc
    path_parsed = parsed.path
    full_path = f"{netloc_parsed}{path_parsed}"
    clean_full_path = full_path.rstrip("/")
    return clean_full_path

def is_same_domain(base_url, current_url):
    base_parts = urlsplit(base_url)
    current_parts = urlsplit(current_url)
    # Return whether the two `.netloc` values are equal
    return base_parts.netloc == current_parts.netloc

def get_html(url):
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    content_type = response.headers["Content-Type"]

    if response.status_code > 400:
        raise Exception("HTTP status code error level above 400 +")

    if "text/html" not in content_type :
        raise Exception("Content-type header is not text/html")

    return response.text


def extract_page_data(html: str, page_url: str):
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html,page_url),
        "image_urls": get_images_from_html(html,page_url)
    }

class AsyncCrawler:
    def __init__(self, base_url: str, max_concurrency: int, max_pages: int) -> None:
        self.visited = set()
        self.lock = asyncio.Lock()
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data = {}
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()
        # initialize the other required fields

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False
            # check self.visited, then add when appropriate
            if normalized_url in self.visited:
                return False

            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False

            self.visited.add(normalized_url)
            return True



    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_html(self, url):
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            html_code = response.status
            html_content = response.headers["Content-Type"]
            html = await response.text()

            # recreating two checks from your old synchronous version
            if html_code > 400:
                raise Exception("HTTP status code error level above 400 +")

            if "text/html" not in html_content:
                raise Exception("Content-type header is not text/html")

            return html

    async def crawl_page(self, current_url):
        if self.should_stop:
            return

        normalized_url = normalize_url(current_url)
        is_new_page = await self.add_page_visit(normalized_url)

        if not is_new_page:
            return

        async with self.semaphore:
           html = await self.get_html(current_url)
           print(f"crawling: {current_url}")
        page_data = extract_page_data(html,current_url)


        async with self.lock:
            self.page_data[normalized_url] = page_data

        outgoing_links = page_data["outgoing_links"]

        tasks = []

        for link in outgoing_links:
            task = asyncio.create_task(self.crawl_page(link))
            tasks.append(task)
            self.all_tasks.add(task)
        try:
            await asyncio.gather(*tasks)
        finally:
            for task in tasks:
                self.all_tasks.discard(task)



    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        result = await crawler.crawl()
        return result

def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url

    if page_data is None:
        page_data = {}

    if not is_same_domain (base_url, current_url):
        return

    # “home → products → home” from looping forever.
    normalized_url = normalize_url(current_url)

    if normalized_url in page_data:
        return

    print(f"crawling: {current_url}")
    html = get_html(current_url)

    data = extract_page_data(html, current_url)
    page_data[normalized_url] = data

    for x in data["outgoing_links"]:
        crawl_page(base_url,x,page_data)

    return page_data