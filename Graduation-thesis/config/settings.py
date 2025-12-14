import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        # Основные URL (уберите лишние пробелы в конце!)
        self.BASE_URL = "https://www.kinopoisk.ru"
        self.API_URL = "https://api.kinopoisk.dev/v1.4"

        # API ключ
        self.API_KEY = os.getenv("KINOPOISK_API_KEY", "FQ1Y3JB-N9F43BE-PJ92X41-7BW07GB")

        # Авторизация
        self.LOGIN = os.getenv("KINOPOISK_LOGIN", "ira_balakovo_@mail.ru")
        self.PASSWORD = os.getenv("KINOPOISK_PASSWORD", "D3kjv0brgblh.")

        # Браузер
        self.BROWSER = os.getenv("BROWSER", "chrome")
        self.HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
        self.TIMEOUT = int(os.getenv("TIMEOUT", "15"))
        self.IMPLICITLY_WAIT = int(os.getenv("IMPLICITLY_WAIT", "10"))

        # Пути
        self.LOGIN_PATH = "/passport"
        self.SEARCH_PATH = "/index.php"
        self.PROFILE_PATH = "/mykp"

        # Тесты
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
        self.RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))


settings = Settings()