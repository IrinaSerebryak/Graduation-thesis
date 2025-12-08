import pytest
import allure
from datetime import datetime


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                screenshot_name = f"screenshot_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                driver.save_screenshot(f"allure-results/{screenshot_name}")
                allure.attach.file(
                    f"allure-results/{screenshot_name}",
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")


@pytest.fixture
def skip_if_no_api_key(api_key_available):
    """Фикстура для пропуска тестов без API ключа"""
    return api_key_available