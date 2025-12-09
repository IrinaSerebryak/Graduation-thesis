from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
import time


class BasePage:
    """Базовый класс для всех Page Objects"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.implicitly_wait(5)

    @allure.step("Открыть URL: {url}")
    def open(self, url: str) -> None:
        """Открыть указанный URL"""
        self.driver.get(url)
        self.wait_page_loaded()

    @allure.step("Дождаться загрузки страницы")
    def wait_page_loaded(self, timeout: int = 30) -> bool:
        """Ожидание полной загрузки страницы"""
        try:
            self.wait.until(
                lambda driver: driver.execute_script(
                    "return document.readyState") == "complete"
            )
            # Дополнительное ожидание для динамического контента
            time.sleep(1)
            return True
        except TimeoutException:
            allure.attach("Страница не загрузилась за отведенное время",
                          name="Page Load Timeout")
            return False

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator: tuple, timeout: int = 10) -> object:
        """Найти элемент с ожиданием"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(*locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"Элемент {locator} не найден за {timeout} секунд")

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator: tuple, timeout: int = 10) -> list:
        """Найти все элементы с ожиданием"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(*locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator: tuple) -> None:
        """Кликнуть по элементу"""
        element = self.find_element(locator)
        try:
            element.click()
        except:
            # Резервный вариант через JavaScript
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст '{text}' в элемент: {locator}")
    def type_text(self, locator: tuple, text: str, clear: bool = True) -> None:
        """Ввести текст в поле"""
        element = self.find_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator: tuple) -> str:
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text.strip()

    @allure.step("Получить атрибут '{attribute}' элемента: {locator}")
    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Получить атрибут элемента"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """Проверить видимость элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Прокрутить до элемента: {locator}")
    def scroll_to_element(self, locator: tuple) -> None:
        """Прокрутить страницу до элемента"""
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )
        time.sleep(0.5)

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str = "screenshot") -> str:
        """Сделать скриншот"""
        filename = f"allure-results/{name}_{int(time.time())}.png"
        self.driver.save_screenshot(filename)
        return filename

    @allure.step("Ожидать появления текста '{text}' на странице")
    def wait_for_text(self, text: str, timeout: int = 10) -> bool:
        """Ожидать появления текста на странице"""
        try:
            self.wait.until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text)
            )
            return True
        except TimeoutException:
            return False