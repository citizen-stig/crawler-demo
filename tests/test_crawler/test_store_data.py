from unittest import mock
from pytest_mock import MockerFixture

from crawler.executor import Crawler


def test_store_data(mocker: MockerFixture):
    crawler = Crawler('https://project-plato.com', '/tmp/abc')

    link = 'https://project-plato/path/to/something'
    data = b'<html>Hi</html>'

    os_mock = mocker.patch('crawler.executor.os')
    os_mock.path.join.return_value = full_path = '/tmp/mock-dir/full-path'
    os_mock.path.dirname.return_value = dir_name = '/tmp/mock-dir'

    m = mock.mock_open()
    with mock.patch('crawler.executor.open', m):
        crawler._store_data(link, data)

    os_mock.path.join.assert_called_once_with('/tmp/abc', 'path/to/something')
    os_mock.makedirs.assert_called_once_with(dir_name, exist_ok=True)

    m.assert_called_once_with(full_path, 'wb')
    handle = m()
    handle.write.assert_called_once_with(data)
