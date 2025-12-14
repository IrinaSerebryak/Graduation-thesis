from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class MainPage(BasePage):
    """Page Object для главной страницы приложения"""

    # Локаторы главной страницы
    LOGO = (By.CSS_SELECTOR, "a.styles_root__nHwYq[href='/']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.styles_input__nBdKx")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.styles_searchButton__vTv_i")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[href*='passport']")
    PROFILE_BUTTON = (By.CSS_SELECTOR, "a[href*='my kp']")

    # Навигация
    FILMS_LINK = (By.LINK_TEXT, "Фильмы")
    SERIES_LINK = (By.LINK_TEXT, "Сериалы")
    CARTOONS_LINK = (By.LINK_TEXT, "Мультфильмы")
    TOP_250_LINK = (By.LINK_TEXT, "Топ 250")
    PREMIERES_LINK = (By.LINK_TEXT, "Скоро в кино")

    # Баннеры и промо
    PROMO_BANNER = (By.CSS_SELECTOR, ".promo-banner")
    FILM_OF_THE_DAY = (By.CSS_SELECTOR, ".film-of-the-day")

    @allure.step("Выполнить поиск: '{query}'")
    def search(self, query: str):
        """Выполнить поиск на главной странице"""
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    @allure.step("Перейти на страницу входа")
    def go_to_login(self):
        """Перейти на страницу входа"""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Перейти в профиль")
    def go_to_profile(self):
        """Перейти в профиль пользователя"""
        if self.is_element_visible(self.PROFILE_BUTTON):
            self.click(self.PROFILE_BUTTON)
        else:
            self.click(self.LOGIN_BUTTON)

    @allure.step("Перейти в раздел 'Фильмы'")
    def go_to_films(self):
        """Перейти в раздел фильмов"""
        self.click(self.FILMS_LINK)

    @allure.step("Перейти в раздел 'Топ 250'")
    def go_to_top250(self):
        """Перейти в раздел Топ 250"""
        self.click(self.TOP_250_LINK)

    @allure.step("Получить placeholder поля поиска")
    def get_search_placeholder(self) -> str:
        """Получить placeholder поля поиска"""
        return self.get_attribute(self.SEARCH_INPUT, "placeholder") or ""

    @allure.step("Проверить наличие логотипа")
    def is_logo_visible(self) -> bool:
        """Проверить видимость логотипа"""
        return self.is_element_visible(self.LOGO)

    @allure.step("Проверить наличие кнопки входа")
    def is_login_button_visible(self) -> bool:
        """Проверить видимость кнопки входа"""
        return self.is_element_visible(self.LOGIN_BUTTON)