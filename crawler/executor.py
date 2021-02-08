import logging
import os
from urllib.parse import urlparse

import requests

from crawler import utils

logger = logging.getLogger('crawler.executor')


class Crawler:
    """Crawler performs fetching data and maintaining visited links"""

    def __init__(self, start_url: str, out_dir: str):
        if not start_url.startswith('http'):
            start_url = 'http://' + start_url
        self.start_url = urlparse(start_url)
        self.out_dir = out_dir
        self._visited_urls = set()
        self._to_visit = {start_url}

    def run(self):
        logger.info("Starting crawler")
        while self._to_visit:
            self._run()

    def _run(self):
        link = self._to_visit.pop()
        response = requests.get(link)
        self._visited_urls.add(link)
        if response.status_code == 200:
            page = response.content.decode('utf-8')
            self._lookup_links(page)
            self._store_data(link, page)
        else:
            logger.error('Response code from url %s is: %s',
                         link, response.status_code)
            logger.error('Data: %s', response.content)

    def _lookup_links(self, page):
        """Extracts all URLs from the page.

        Checks if they should be visited and updates self._to_visit"""
        links = utils.extract_links(page)
        for link in links:
            if link.startswith('/'):
                link = self.start_url.scheme + "://" + self.start_url.netloc + link
            parsed_link = urlparse(link)
            if parsed_link.netloc != self.start_url.netloc:
                continue
            if not parsed_link.path.startswith(self.start_url.path):
                continue
            if link in self._visited_urls:
                continue
            logger.debug("New link to visit: %s", link)
            self._to_visit.add(link)

    def _store_data(self, link: str, page_data: str):
        """Dumps data to appropriate path in output directory"""
        logger.debug('this is link: "%s"', link)
        parsed_url = urlparse(link)
        if parsed_url.path == '/' or parsed_url.path == '':
            sub_path = 'index.html'
        else:
            sub_path = parsed_url.path[1:]
        full_path = os.path.join(self.out_dir, sub_path)
        logger.info("Going to save %s symbols to %s",
                    len(page_data),
                    full_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as out_file:
            out_file.write(page_data)
