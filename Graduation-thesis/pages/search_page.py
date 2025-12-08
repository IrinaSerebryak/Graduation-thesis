from selenium.webdriver.common.by import By
from base_page import BasePage
import allure


class SearchPage(BasePage):
    # Локаторы страницы поиска
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search_results .element")
    SEARCH_RESULT_TITLES = (By.CSS_SELECTOR, ".search_results .name a")
    SEARCH_RESULT_YEARS = (By.CSS_SELECTOR, ".search_results .year")
    SEARCH_RESULT_RATINGS = (By.CSS_SELECTOR, ".rating")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".search_results .empty")
    SEARCH_FILTERS = (By.CSS_SELECTOR, ".search_filters")
    FILM_TYPE_FILTER = (By.CSS_SELECTOR, "input[name='m_act[type]'][value='film']")
    SERIES_TYPE_FILTER = (By.CSS_SELECTOR, "input[name='m_act[type]'][value='tv_series']")

    @allure.step("Получить количество результатов поиска")
    def get_results_count(self) -> int:
        """Получить количество найденных результатов"""
        elements = self.find_elements(self.SEARCH_RESULTS)
        return len(elements)

    @allure.step("Получить названия найденных фильмов")
    def get_result_titles(self) -> list:
        """Получить список названий найденных фильмов"""
        elements = self.find_elements(self.SEARCH_RESULT_TITLES)
        return [el.text for el in elements]

    @allure.step("Получить годы выпуска найденных фильмов")
    def get_result_years(self) -> list:
        """Получить список годов выпуска найденных фильмов"""
        elements = self.find_elements(self.SEARCH_RESULT_YEARS)
        return [el.text for el in elements]

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

    @allure.step("Проверить сообщение 'ничего не найдено'")
    def is_no_results_message_displayed(self) -> bool:
        """Проверить отображение сообщения об отсутствии результатов"""
        return self.is_element_visible(self.NO_RESULTS_MESSAGE)