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

def main():
    print("Hello from build-a-web-scraper!")


if __name__ == "__main__":
    main()
