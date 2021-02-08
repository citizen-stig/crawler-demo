from typing import Set

from bs4 import BeautifulSoup


def extract_links(page: str) -> Set[str]:
    """Returns all http links from data

    Note: only links inside <a> tag is found.
    Plain text links are not searched
    Relative links as well
    """
    soup = BeautifulSoup(page, 'html.parser')

    urls = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            urls.add(href)

    return urls
