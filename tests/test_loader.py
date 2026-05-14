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


def test_get_status_returns_int():
    """
    Проверяем, что get_status возвращает целое число.
    """
    loader = WebDataLoader("https://this.url.does.not.exist.local")
    result = loader.get_status("/api")

    # Статус должен быть числом (0, 200, 404 и т.д)
    assert isinstance(result, int)
    print(f"ТЕСТ ПРОЙДЕН: Статус - целое число ({result}).")
