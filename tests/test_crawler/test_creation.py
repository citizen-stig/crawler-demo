import pytest

from crawler.executor import Crawler


def test_created_successfully():
    c = Crawler('https://project-plato.com', '/tmp/project-plato')
    assert c.start_url.netloc == 'project-plato.com'
    assert c.out_dir == '/tmp/project-plato'

    Crawler('https://project-plato.com/some-path', '/tmp/project-plato')
    Crawler('project-plato.com/some-path', '/tmp/project-plato')
