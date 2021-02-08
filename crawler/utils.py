# import re
from typing import Set

from bs4 import BeautifulSoup

# url_regex = re.compile('(?:https?://)?(?:[\w]+\.)(?:\.?[\w]{2,})+')


def extract_links(page: str) -> Set[str]:
    """Returns all http links from data

    Relative links as well
    """
    soup = BeautifulSoup(page, 'html.parser')

    urls = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            urls.add(href)

    return urls
