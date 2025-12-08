import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Основные URL
    BASE_URL = "https://www.kinopoisk.ru"
    API_URL = "https://api.kinopoisk.dev/v1.4"

    # API ключ (получить на https://api.kinopoisk.dev/)
    API_KEY = os.getenv("KINOPOISK_API_KEY", "")

    # Настройки браузера
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "15"))
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))

    # Тестовые данные
    TEST_EMAIL = os.getenv("TEST_EMAIL", "")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")

    # Пути
    LOGIN_PATH = "/passport"
    SEARCH_PATH = "/index.php"


settings = Settings()