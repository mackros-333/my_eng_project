import requests


class WebDataLoader:
    """
    Класс для безопасной загрузки данных из интернета.
    Не падает с ошибкой, если сервер недоступен.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def load_json(self, path):
        full_url = self.base_url + path
        print(f"Пытаюсь подключиться к {full_url}")

        try:
            response = requests.get(full_url, timeout=5)
            if response.status_code == 200:
                print("Данные успешно получены!")
                return response.json()
            else:
                print(f"Сервер ответил статусом: {response.status_code}")
                return dict()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}")
            return dict()