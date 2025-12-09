import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Основные URL
    BASE_URL = "https://www.kinopoisk.ru"
    API_URL = "https://api.kinopoisk.dev/v1.4"

    # API ключ (ваш токен)
    API_KEY = os.getenv("KINOPOISK_API_KEY", "FQ1Y3JB-N9F43BE-PJ92X41-7BW07GB")

    # Данные для авторизации на сайте
    LOGIN = os.getenv("KINOPOISK_LOGIN", "ira_balakovo_@mail.ru")
    PASSWORD = os.getenv("KINOPOISK_PASSWORD", "D3kjv0brgblh.")

    # Настройки браузера
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "15"))
    IMPLICITLY_WAIT = int(os.getenv("IMPLICITLY_WAIT", "10"))

    # Пути
    LOGIN_PATH = "/passport"
    SEARCH_PATH = "/index.php"
    PROFILE_PATH = "/mykp"

    # Настройки тестов
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))


settings = Settings()