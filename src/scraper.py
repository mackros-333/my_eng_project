import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


class BookScraper:
    """
    Сборщик книг с сайта book.toscrape.com
    Обходит все страницы каталога и собирает:
    - название книги
    - цену
    - рейтинг (звёзды)
    """

    def __init__(self):
        # Адерс сайта который будем грабить
        self.base_url = "https://books.toscrape.com"
        # А сюда будем складывать все найденные книги
        self.all_books = []

    def scrape_one_page(self, page_url):
        """
        Загружает одну страницу каталога и собирает с неё книги.
        Возвращая список книг с этой страницы.
        """
        print(f"Загружаю страницу: {page_url}")

        try:
            # идём за страницей
            response = requests.get(page_url, timeout=10)

            if response.status_code != 200:
                print(f"Ошибка! Статус: {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, "lxml")

            # Находим все книги на странице.
            # Каждая книга лежит в теге <article class="product_pod">
            books_on_page = []
            articles = soup.find_all("article", class_="product_pod")

            for book in articles:
                # --- Добываем название ---
                # Название лежит в теге <h3> -> <a title="..."
                title_tag = book.h3.a
                title = title_tag.get("title", "Без названия")

                # --- Добываем цену ---
                # Цена лежит в теге <p class="Price_color">
                price_tag = book.find("p", class_="price_color")
                price = price_tag.get_text(strip=True) if price_tag else "0"

                # --- Добываем цену ---
                # Рейтинг зашит в классе: <p class="star-rating Three">
                # Нам нужно второе слово из класса
                rating_tag = book.find("p", class_="star-rating")
                if rating_tag:
                    # class_ у тега - это список, например ["star-rating", "Three"]
                    rating_class = rating_tag.get("class")
                    # Берём второй элемент списка - сам рейтинг
                    rating = rating_class[1] if len(rating_class) > 1 else "Unknown"
                else:
                    rating = "Unknown"

                # Складываем всё в словарь
                book_data = {"title": title, "price": price, "rating": rating}
                books_on_page.append(book_data)

            print(f"На этой странице собрано книг: {len(books_on_page)}")
            return books_on_page
        except requests.exceptions.RequestException as e:
            print(f"Не могу загрузить страницу: {e}")
            return []

    def scrape_all_pages(self):
        """
        Обходит все страницы каталога (1-50).
        На каждой странице находит ссылку "next" и идёт дальше.
        """
        # Начиная с первой страницы
        current_url = self.base_url + "/catalogue/page-1.html"
        page_number = 1

        while current_url:
            print(f"\n===== Страница {page_number} =====")

            # Собираем книги с текущей страницы
            books = self.scrape_one_page(current_url)
            self.all_books.extend(books)  # Добавляем в общую копилку

            # Ищем кнопку "next" - ссылку на следующую страницу
            try:
                responce = requests.get(current_url, timeout=10)
                soup = BeautifulSoup(responce.text, "lxml")

                # Кнопка "next" лежит в <li class="next"> -> <a href="..."
                next_button = soup.find("li", class_="next")

                if next_button:
                    # Берём относительную ссылку (например, "page-2.html")
                    next_link = next_button.a.get("href")
                    # Превращаем в полный адрес
                    current_url = self.base_url + "/catalogue/" + next_link
                    page_number += 1
                    # Задуржка 1 сек - вежливость к серверу
                    time.sleep(1)
                else:
                    # Кнопки "next" нет - значит, это последняя страница
                    print("Достигнут конец каталога.")
                    current_url = None

            except Exception as e:
                print(f"Ошибка при поиске следующей страницы: {e}")
                current_url = None

        print(f"\nВсего собрано книг: {len(self.all_books)}")

    def save_to_csv(self, filename="books.csv"):
        """
        Сохраняет всесобранные книги в CSV-файл.
        Этот файл можно открыть в Excel.
        """
        if not self.all_books:
            print("Нечего сохранять. Сначала запустите scrape_all_pages().")
            return

        # Превращаем список словарей в таблицу pandas
        df = pd.DataFrame(self.all_books)
        # Сохраняем  CSV
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"Сохранено {len(self.all_books)} книг в файл '{filename}'")
