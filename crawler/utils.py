# import re
from typing import Set

from bs4 import BeautifulSoup

# url_regex = re.compile('(?:https?://)?(?:[\w]+\.)(?:\.?[\w]{2,})+')


def extract_links(page: str) -> Set[str]:
    soup = BeautifulSoup(page, 'html.parser')

    urls = set()
    for link in soup.find_all('a'):
        urls.add(link.get('href'))

    return urls
