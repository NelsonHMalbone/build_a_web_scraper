from urllib.parse import urlsplit

def normalize_url(url):
    parsed =urlsplit(url)
    netloc_parsed = parsed.netloc
    path_parsed = parsed.path
    full_path = f"{netloc_parsed}{path_parsed}"
    clean_full_path = full_path.rstrip("/")
    return clean_full_path