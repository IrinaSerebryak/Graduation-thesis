from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть страницу {url}")
    def open(self, url: str) -> None:
        """Открыть указанный URL"""
        self.driver.get(url)
        self.wait_page_loaded()

    @allure.step("Дождаться загрузки страницы")
    def wait_page_loaded(self, timeout: int = 30) -> bool:
        """Ожидание загрузки страницы"""
        try:
            self.wait.until(
                lambda driver: driver.execute_script(
                    "return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: tuple, timeout: int = 15) -> object:
        """Найти элемент с ожиданием"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(*locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"Элемент {locator} не найден за {timeout} секунд")

    @allure.step("Найти элементы {locator}")
    def find_elements(self, locator: tuple, timeout: int = 15) -> list:
        """Найти все элементы с ожиданием"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(*locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    @allure.step("Кликнуть по элементу {locator}")
    def click(self, locator: tuple) -> None:
        """Кликнуть по элементу"""
        element = self.find_element(locator)
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст '{text}' в поле {locator}")
    def type_text(self, locator: tuple, text: str, clear: bool = True) -> None:
        """Ввести текст в поле"""
        element = self.find_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator: tuple) -> str:
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text.strip()

    @allure.step("Получить атрибут '{attr}' элемента {locator}")
    def get_attribute(self, locator: tuple, attr: str) -> str:
        """Получить атрибут элемента"""
        element = self.find_element(locator)
        return element.get_attribute(attr)

    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """Проверить видимость элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(*locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str) -> None:
        """Сделать скриншот"""
        self.driver.save_screenshot(f"screenshots/{name}.png")

    @allure.step("Прокрутить до элемента {locator}")
    def scroll_to_element(self, locator: tuple) -> None:
        """Прокрутить страницу до элемента"""
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )
        time.sleep(0.5)