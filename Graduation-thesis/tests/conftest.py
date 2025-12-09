import pytest
import allure
import os
from datetime import datetime
from config.settings import settings


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            # Создаем папку для скриншотов если её нет
            if not os.path.exists("allure-results"):
                os.makedirs("allure-results")

            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                screenshot_name = f"screenshot_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = f"allure-results/{screenshot_name}"
                driver.save_screenshot(screenshot_path)

                allure.attach.file(
                    screenshot_path,
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")


@pytest.fixture(scope="session")
def api_key_available():
    """Фикстура проверки доступности API ключа"""
    if not settings.API_KEY or settings.API_KEY == "ваш_ключ_здесь":
        pytest.skip("API ключ не установлен. Установите KINOPOISK_API_KEY в .env файле")
    return True


@pytest.fixture
def skip_if_no_api_key(api_key_available):
    """Фикстура для пропуска тестов без API ключа"""
    return api_key_available