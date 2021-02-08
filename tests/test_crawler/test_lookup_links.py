from typing import Set

from pytest_mock import MockerFixture

from crawler.executor import Crawler


# def check_new_urls_added


def check_lookup(mocker: MockerFixture,
                 start_url: str,
                 extracted: Set[str],
                 expected: Set[str]):
    crawler = Crawler(start_url, '/tmp/abc')
    crawler._visited_urls = {start_url}
    crawler._to_visit = set()

    utils_mock = mocker.patch('crawler.executor.utils')
    utils_mock.extract_links.return_value = extracted

    crawler._lookup_links("")

    assert len(crawler._to_visit) == len(expected)
    assert expected.issubset(crawler._to_visit)

    utils_mock.reset_mock()


def test_adds_new_links(mocker: MockerFixture):
    check_lookup(
        mocker,
        'https://project-plato.com/abc',
        {
            'https://project-plato.com/abc',
            'https://project-plato.com/abc/de',
            'https://project-plato.com/abc/fh'
        },
        {
            'https://project-plato.com/abc/de',
            'https://project-plato.com/abc/fh'
        })


def test_prepends_hostname(mocker: MockerFixture):
    check_lookup(
        mocker,
        'https://project-plato.com/abc',
        {
            'https://project-plato.com/abc/de',
            '/abc/fh'
        },
        {
            'https://project-plato.com/abc/de',
            'https://project-plato.com/abc/fh',
        })


def test_do_not_adds_another_domain(mocker: MockerFixture):
    check_lookup(
        mocker,
        'https://project-plato.com/abc',
        {
            'https://project-plato.com/abc/de',
            'https://example.com/abc/fh'
        },
        {
            'https://project-plato.com/abc/de',
        })


def test_do_not_add_another_sub_path(mocker: MockerFixture):
    check_lookup(
        mocker,
        'https://project-plato.com/abc',
        {
            'https://project-plato.com/abc/de',
            'https://project-plato.com/xyz/de',
        },
        {
            'https://project-plato.com/abc/de',
        })

    check_lookup(
        mocker,
        'https://project-plato.com',
        {
            'https://project-plato.com/abc/de',
            'https://project-plato.com/xyz/de',
        },
        {
            'https://project-plato.com/abc/de',
            'https://project-plato.com/xyz/de',
        })
