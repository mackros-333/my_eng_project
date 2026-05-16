import requests
from bs4 import BeautifulSoup


class SimpleParser:
    """
    Парсер веб станиц.
    Умеет находить все заголовки и ссылки на странице.
    """

    def __init__(self, url):
        self.url = url
        self.soup = None

    def feth_page(self):
        """
        Скачивает страницу и готовит к разбору.
        Возвращает True, если успешно.
        """
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.text, "lxml")
                print(f"Страница {self.url} загружена.")
                return True
            else:
                print(f"Ошибка загрузки: статус {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Не могу подключиться: {e}")
            return False

    def get_all_links(self):
        """
        Возвращает список всех ссылок со страницы.
        """
        if not self.soup:
            print("Сначала загрузите страницу (feth_page).")
            return []

        links = []
        for tag in self.soup.find_all("a", href=True):
            links.append(tag["href"])
        print(f"Найдено ссылок: {len(links)}")
        return links

    def get_all_headers(self):
        """
        Возвращает все заголоввки h1-h3.
        """
        if not self.soup:
            print("Сначала загрузите страницу (feth_page).")
            return []

        headers = []
        for level in ["h1", "h2", "h3"]:
            for tag in self.soup.find_all(level):
                headers.append({"level1": level, "text": tag.get_text(strip=True)})
                print(f"Найдено заголовков: {len(headers)}")
                return headers

    def get_books(self):
        if not self.soup:
            print("Сначала загрузите страницу (feth_page).")
            return []
