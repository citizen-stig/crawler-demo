import pytest

from crawler.utils import extract_links


def test_extract_urls_from_href():
    page = """
    <a href="http://example.com/test">click me</a>
    <a href="/about-us">about</a>
    """

    urls = extract_links(page)
    assert len(urls) == 2
    assert "http://example.com/test" in urls
    assert "/about-us" in urls


@pytest.mark.skip(reason="To be implemented")
def test_extract_urls_from_plain_text():
    page = """
        <p>Visit http://example.com/test2 to know more or https://ya.ru/search</p>
        <p>Also http://your.shop/cart for more!</p>
        <p> thisisnothttp://ya.ru/even it look like one</p>
        <p> but amazon.com is shurele a link</a>
        <a href="/about-us">about</a>
        """

    urls = extract_links(page)
    assert len(urls) == 4
    assert "http://example.com/test2" in urls
    assert "/about-us" in urls
    assert "https://ya.ru/search" in urls
    assert "http://your.shop/cart" in urls


@pytest.mark.skip(reason="To be implemented")
def test_excludes_non_anchor():
    page = """
       <a href="http://example.com/test">click me</a>
       <a href="#about-us">about</a>
       <a onclick="something() href="">check</a>
       """
    urls = extract_links(page)
    assert len(urls) == 1
    assert "http://example.com/test2" in urls


@pytest.mark.skip(reason="To be implemented")
def test_excludes_non_web():
    page = """
        <a href="http://example.com/test">click me</a>
        <a href="mailto:someone@example.com">mail us</a>
        <a href="skype:someone>call us</a>
        <a href="tel:+4733378901>call us here to</a>
        <a href="javascript:alert('Hello World!');">click</a>
    """

    urls = extract_links(page)
    assert len(urls) == 1
    assert "http://example.com/test2" in urls
