from urllib.parse import urljoin
from typing import TypedDict

from bs4 import BeautifulSoup, Tag


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


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

def extract_page_data(html: str, page_url: str):
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html,page_url),
        "image_urls": get_images_from_html(html,page_url)
    }

# the code above is just the set up
def main():
    print("Hello from build-a-web-scraper!")


if __name__ == "__main__":
    main()
