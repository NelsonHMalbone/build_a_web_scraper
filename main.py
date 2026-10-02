from typing import TypedDict
import sys
import asyncio

from crawl import crawl_site_async

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

# the code above is just the set up
async def main():
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

    page_data = await crawl_site_async(BASE_URL)
    print(f"pages found: {len(page_data)}")

    for page in page_data.values():
        print(page)


if __name__ == "__main__":
    asyncio.run(main())
