

class Crawler:

    def __init__(self, start_url: str, out_dir: str):
        self.start_url = start_url
        self.out_dir = out_dir
        self._visited_urls = set()
        self._to_visit = {self.start_url}

    def run(self):
        pass

    def _lookup_links(self, page):
        """Extracts all URLs from the page.

        Checks if they should be visited and updates self._to_visit"""
        pass

    def _store_data(self, url, page_data):
        """Dumps data to output folder"""
        pass
