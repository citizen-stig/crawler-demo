import logging
import os
from collections import Set
from urllib.parse import urlparse
import threading

import requests

from crawler import utils

logger = logging.getLogger('crawler.executor')


class Crawler:
    """Crawler performs fetching data and maintaining visited links"""
    thread_count = 12

    def __init__(self, start_url: str, out_dir: str):
        if not start_url.startswith('http'):
            start_url = 'http://' + start_url
        self.start_url = urlparse(start_url)
        self.out_dir = out_dir
        self._visited_urls: Set[str] = set()
        self._to_visit = {start_url}
        self._stop = False

    def run(self):
        """Start crawler"""
        logger.info("Starting crawler")

        threads = []
        for _ in range(self.thread_count):
            thread = threading.Thread(target=self._run)
            thread.start()
            threads.append(thread)

        for thread in threads:
            try:
                thread.join()
            except KeyboardInterrupt:
                self._stop = True
                logger.info('Stopping...')

    def _run(self):
        while self._to_visit and not self._stop:
            link = self._to_visit.pop()
            logger.debug("Going to request: %s", link)
            if link is None:
                break
            response = requests.get(link)
            self._visited_urls.add(link)
            if response.status_code == 200:
                content = response.content
                try:
                    page = content.decode('utf-8')
                    self._lookup_links(page)
                except UnicodeDecodeError:
                    logger.debug('Cannot decode response from %s', link)
                self._store_data(link, content)
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
                link = self.start_url.scheme \
                       + "://" \
                       + self.start_url.netloc \
                       + link
            parsed_link = urlparse(link)
            if parsed_link.netloc != self.start_url.netloc:
                continue
            if not parsed_link.path.startswith(self.start_url.path):
                continue
            if link in self._visited_urls:
                continue
            self._to_visit.add(link)

    def _store_data(self, link: str, page_data: bytes):
        """Dumps data to appropriate path in output directory"""
        parsed_url = urlparse(link)
        if parsed_url.path == '' or parsed_url.path.endswith('/'):
            sub_path = parsed_url.path[1:] + 'index.html'
        else:
            sub_path = parsed_url.path[1:]
        full_path = os.path.join(self.out_dir, sub_path)
        logger.info("Going to save %s symbols to %s",
                    len(page_data),
                    full_path)
        self._make_dirs(os.path.dirname(full_path))
        if os.path.isdir(full_path):
            full_path = os.path.join(full_path, 'index.html')
        with open(full_path, 'wb') as out_file:
            out_file.write(page_data)

    @staticmethod
    def _make_dirs(dir_name):
        current_dir_name = dir_name
        while current_dir_name:
            if os.path.isfile(current_dir_name):
                logger.info('path %s is file, renaming...', current_dir_name)
                tmp_name = current_dir_name + '.tmp'
                os.rename(current_dir_name, tmp_name)
                os.makedirs(dir_name, exist_ok=True)
                os.rename(tmp_name,
                          os.path.join(current_dir_name, 'index.html'))
            current_dir_name, rest = os.path.split(current_dir_name)
        os.makedirs(dir_name, exist_ok=True)
