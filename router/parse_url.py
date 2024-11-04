from urllib.parse import urlparse

def normalize_url(url, use_https=False):
    parsed_url = urlparse(url)
    scheme = ""
    if not parsed_url.scheme:
        scheme = 'https://' if use_https else 'http://'

    if not parsed_url.netloc[:4] == "www." :
        url = 'www.' + url

    if parsed_url.path.endswith("/"):
        url = url[:-1]
        
    return f'{scheme}{url}'
