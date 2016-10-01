from urllib.parse import urljoin, urlunsplit, urlsplit


def clean_text(texts):
    return filter(
        None,
        [text.strip(' \r\n\t\xa0') for text in texts]
    )


def clean_url(urls, base_url):
    cleaned_urls = set()
    for url in urls:
        url = urljoin(base_url, url)
        fragments = urlsplit(url)
        if fragments.scheme == 'http' or fragments.scheme == 'https':
            new_fragments = fragments[:4] + ('',)
            cleaned_url = urlunsplit(new_fragments)
            cleaned_urls.add(cleaned_url)
    return cleaned_urls
