# Файл запуска сборщика книг.
# Просто запускаем этот файл и он всё сделает.

from src.scraper import BookScraper

# Создаём сборщик
scraper = BookScraper()

# Запускаем обход всех 50 страниц (займёт около 1 минуты)
print("Начинаю сбор книг. Это займёт около минуты...")
scraper.scrape_all_pages()

# Сохраняем результат в CSV
scraper.save_to_csv("books.csv")
print("Готово! Откройте books.csv в Excel")