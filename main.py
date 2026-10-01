from typing import TypedDict
import sys

from crawl import crawl_page

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

# the code above is just the set up
def main():
    print("Hello from build-a-web-scraper!")

    #setting up some arguments
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    BASE_URL = sys.argv[1]

    if len(sys.argv) == 2:
        print(f"starting crawl of: {BASE_URL}")

    crawl_pages = crawl_page(BASE_URL)
    print(f"pages found: {len(crawl_pages)}")

if __name__ == "__main__":
    main()
