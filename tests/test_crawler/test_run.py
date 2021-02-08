from pytest_mock import MockerFixture

from crawler.executor import Crawler


def test_run_threads(mocker: MockerFixture):
    c = Crawler('https://project-plato.com', '/tmp/project-plato')
    c._to_visit.add('https://project-plato.com/a')
    c._to_visit.add('https://project-plato.com/b')

    c._lookup_links = mocker.Mock()
    c._store_data = mocker.Mock()

    mock_req = mocker.patch('crawler.executor.requests')
    mock_req.get.return_value = response_mock = mocker.Mock()
    response_mock.status_code = 200
    response_mock.content = b'<html>hi</html>'

    c.run()

    assert len(c._visited_urls) == 3
    assert c._lookup_links.call_count == 3
    c._lookup_links.assert_called_with('<html>hi</html>')
    assert c._store_data.call_count == 3
    c._store_data.assert_any_call('https://project-plato.com',
                                  b'<html>hi</html>')
    c._store_data.assert_any_call('https://project-plato.com/a',
                                  b'<html>hi</html>')
    c._store_data.assert_any_call('https://project-plato.com/b',
                                  b'<html>hi</html>')


def test_respects_stopped_flag(mocker):
    c = Crawler('https://project-plato.com', '/tmp/project-plato')
    c._stop = True
    c._lookup_links = mocker.Mock()
    c._store_data = mocker.Mock()
    mock_req = mocker.patch('crawler.executor.requests')
    mock_req.get.return_value = mocker.Mock()

    c.run()

    assert len(c._visited_urls) == 0
    assert c._lookup_links.call_count == 0
    assert c._store_data.call_count == 0

