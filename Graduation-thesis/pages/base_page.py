from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import allure
import time


class BasePage:
    """Базовый класс для всех Page Objects"""

    def __init__(self, driver):
        self.driver = driver
        self.default_wait = WebDriverWait(driver, 10)

    @allure.step("Открыть URL: {url}")
    def open(self, url: str):
        """Открыть указанный URL"""
        self.driver.get(url)
        self.wait_page_loaded()

    @allure.step("Дождаться загрузки страницы")
    def wait_page_loaded(self, timeout: int = 30) -> bool:
        """Ожидание полной загрузки страницы (document.readyState == 'complete')"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            allure.attach(
                body=self.driver.get_screenshot_as_png(),
                name="Page_Load_Timeout",
                attachment_type=allure.attachment_type.PNG
            )
            return False

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator: tuple, timeout: int = 10):
        """Найти элемент с ожиданием presence (появления в DOM)"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)  # ← locator передаётся как кортеж, БЕЗ *
            )
        except TimeoutException:
            raise NoSuchElementException(f"Элемент не найден за {timeout} сек: {locator}")

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator: tuple, timeout: int = 10):
        """Найти все элементы с ожиданием появления хотя бы одного"""
        try:
            # Ждём появления первого элемента (иначе find_elements вернёт [] сразу)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)  # ← здесь *locator КОРРЕКТЕН (find_elements принимает By, value)
        except TimeoutException:
            return []

    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator: tuple, timeout: int = 10):
        """Кликнуть по элементу после ожидания его кликабельности"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except (TimeoutException, WebDriverException) as C:
            allure.attach(
                body=self.driver.get_screenshot_as_png(),
                name=f"Click_Failed_{locator}",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    @allure.step("Ввести текст '{text}' в элемент: {locator}")
    def type_text(self, locator: tuple, text: str, clear: bool = True, timeout: int = 10):
        """Ввести текст в поле после ожидания его видимости и активности"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        if clear:
            element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator: tuple, timeout: int = 10) -> str:
        """Получить текст элемента (ожидание видимости)"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text.strip()

    @allure.step("Получить атрибут '{attribute}' элемента: {locator}")
    def get_attribute(self, locator: tuple, attribute: str, timeout: int = 10) -> str:
        """Получить атрибут элемента"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element.get_attribute(attribute) or ""

    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """Проверить, виден ли элемент на странице"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Прокрутить до элемента: {locator}")
    def scroll_to_element(self, locator: tuple, timeout: int = 10):
        """Прокрутить страницу до элемента и дождаться его появления"""
        element = self.find_element(locator, timeout=timeout)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
            element
        )
        # Дать время на анимацию/загрузку
        WebDriverWait(self.driver, 2).until(
            EC.visibility_of(element)
        )

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str = "screenshot") -> str:
        """Сделать скриншот и сохранить в Allure-результаты"""
        timestamp = int(time.time())
        filename = f"allure-results/{name}_{timestamp}.png"
        try:
            self.driver.save_screenshot(filename)
            with open(filename, "rb") as f:
                allure.attach(f.read(), name=name, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")
        return filename

    @allure.step("Ожидать появления текста '{text}' на странице")
    def wait_for_text(self, text: str, timeout: int = 10) -> bool:
        """Ожидать появления текста в <body> (чувствительно к регистру и пробелам!)"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text)
            )
            return True
        except TimeoutException:
            return False