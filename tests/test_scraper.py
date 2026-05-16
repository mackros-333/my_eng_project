from src.scraper import BookScraper


def test_scraper_has_empty_list_at_start():
    """
    Проверяем: при создании сборщика список книг пуст.
    """
    scraper = BookScraper()
    assert scraper.all_books == []
