from urllib.parse import urlparse

from crawler import utils


class Crawler:

    def __init__(self, start_url: str, out_dir: str):
        if not start_url.startswith('http'):
            start_url = 'http://' + start_url
        self.start_url = urlparse(start_url)
        self.out_dir = out_dir
        self._visited_urls = set()
        self._to_visit = {start_url}

    def run(self):
        pass

    def _run(self):
        pass

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
            self._to_visit.add(link)

    def _store_data(self, url, page_data):
        """Dumps data to output folder"""
        pass
