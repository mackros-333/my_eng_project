from src.parser import SimpleParser


def test_feth_fake_url_fails():
    """
    Проверяем: несуществующий URL не загружается.
    """
    parser = SimpleParser("https://this.url.does.not.exist.local")
    result = parser.feth_page()
    assert result is False


def test_get_links_without_feth_returns_empty():
    """
    Проверяем: без загрузки страницы ссылок нет.
    """
    parser = SimpleParser("https://example.com")
    links = parser.get_all_links()
    assert links == []
