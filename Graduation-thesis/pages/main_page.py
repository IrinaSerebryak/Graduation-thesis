from selenium.webdriver.common.by import By
from base_page import BasePage
import allure


class MainPage(BasePage):
    # Локаторы главной страницы Кинопоиска
    LOGO = (By.CSS_SELECTOR, "a[href='/']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='kp_query']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[href*='passport']")
    MENU_ITEMS = (By.CSS_SELECTOR, "nav a")
    FILM_OF_THE_DAY = (By.CSS_SELECTOR, ".film-of-the-day")
    TOP_250 = (By.LINK_TEXT, "Топ 250")
    PREMIERES = (By.LINK_TEXT, "Скоро в кино")
    TRAILERS = (By.LINK_TEXT, "Трейлеры")

    @allure.step("Выполнить поиск: {query}")
    def search(self, query: str) -> None:
        """Выполнить поиск на главной странице"""
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    @allure.step("Перейти на страницу входа")
    def go_to_login(self) -> None:
        """Перейти на страницу входа"""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Перейти в Топ 250")
    def go_to_top250(self) -> None:
        """Перейти в раздел Топ 250"""
        self.click(self.TOP_250)

    @allure.step("Получить текст поля поиска")
    def get_search_placeholder(self) -> str:
        """Получить placeholder поля поиска"""
        return self.get_attribute(self.SEARCH_INPUT, "placeholder")

    @allure.step("Проверить наличие логотипа")
    def is_logo_visible(self) -> bool:
        """Проверить видимость логотипа"""
        return self.is_element_visible(self.LOGO)