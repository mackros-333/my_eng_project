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

    def get_status(self, path):
        """
        Проверяет, доступен ли адрес.
        Возвращает HTTP-статус код (200, 404, 500...).
        Если сервер не отвечает — возвращает 0.
        """
        full_url = self.base_url + path
        print(f"Проверяю статус: {full_url}")

        try:
            response = requests.head(full_url, timeout=5)
            status = response.status_code
            print(f"Статус: {status}")
            return status
        except requests.exceptions.RequestException:
            print("Сервер не отвечает, статус: 0")
            return 0
