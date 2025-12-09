from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class SearchPage(BasePage):
    """Page Object для страницы поиска"""

    # Локаторы страницы поиска
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search_results .element")
    SEARCH_RESULT_TITLES = (By.CSS_SELECTOR, ".search_results .name a")
    SEARCH_RESULT_YEARS = (By.CSS_SELECTOR, ".search_results .year")
    SEARCH_RESULT_RATINGS = (By.CSS_SELECTOR, ".rating")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".search_results .empty")
    SEARCH_FILTERS = (By.CSS_SELECTOR, ".search_filters")

    # Фильтры поиска
    FILM_TYPE_FILTER = (By.CSS_SELECTOR, "input[name='m_act[type]'][value='film']")
    SERIES_TYPE_FILTER = (By.CSS_SELECTOR, "input[name='m_act[type]'][value='tv_series']")
    YEAR_FROM_INPUT = (By.CSS_SELECTOR, "input[name='m_act[year]']")
    YEAR_TO_INPUT = (By.CSS_SELECTOR, "input[name='m_act[to_year]']")
    RATING_FROM_INPUT = (By.CSS_SELECTOR, "input[name='m_act[rating]']")

    @allure.step("Получить количество результатов поиска")
    def get_results_count(self) -> int:
        """Получить количество найденных результатов"""
        elements = self.find_elements(self.SEARCH_RESULTS)
        return len(elements)

    @allure.step("Получить названия найденных фильмов")
    def get_result_titles(self) -> list:
        """Получить список названий найденных фильмов"""
        elements = self.find_elements(self.SEARCH_RESULT_TITLES)
        return [el.text for el in elements[:10]]  # Ограничиваем первыми 10

    @allure.step("Перейти к фильму по индексу {index}")
    def go_to_film_by_index(self, index: int = 0) -> None:
        """Перейти к странице фильма по индексу в результатах поиска"""
        elements = self.find_elements(self.SEARCH_RESULT_TITLES)
        if elements and index < len(elements):
            elements[index].click()

    @allure.step("Применить фильтр 'Только фильмы'")
    def apply_film_filter(self) -> None:
        """Применить фильтр для показа только фильмов"""
        if self.is_element_visible(self.FILM_TYPE_FILTER):
            self.click(self.FILM_TYPE_FILTER)

    @allure.step("Установить фильтр по году с {year_from} по {year_to}")
    def set_year_filter(self, year_from: str, year_to: str) -> None:
        """Установить фильтр по диапазону годов"""
        if self.is_element_visible(self.YEAR_FROM_INPUT):
            self.type_text(self.YEAR_FROM_INPUT, year_from)
            self.type_text(self.YEAR_TO_INPUT, year_to)

    @allure.step("Проверить сообщение 'ничего не найдено'")
    def is_no_results_message_displayed(self) -> bool:
        """Проверить отображение сообщения об отсутствии результатов"""
        return self.is_element_visible(self.NO_RESULTS_MESSAGE)

    @allure.step("Получить текст сообщения об отсутствии результатов")
    def get_no_results_message(self) -> str:
        """Получить текст сообщения об отсутствии результатов"""
        if self.is_no_results_message_displayed():
            return self.get_text(self.NO_RESULTS_MESSAGE)
        return ""