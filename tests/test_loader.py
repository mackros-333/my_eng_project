from src.loader import WebDataLoader


def test_bad_url_returns_empty_dict():
    """
    Проверяем: если адрес кривой, возвращается пустой словарь.
    """
    loader = WebDataLoader("https://this.url.does.not.exist.local")
    result = loader.load_json("/api")

    assert result == dict()
    assert len(result) == 0
    print("ТЕСТ ПРОЙДЕН: Отказоустойчивость работает.")
