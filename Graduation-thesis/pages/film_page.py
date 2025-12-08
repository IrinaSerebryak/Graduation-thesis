from selenium.webdriver.common.by import By
from base_page import BasePage
import allure


class FilmPage(BasePage):
    # Локаторы страницы фильма
    FILM_TITLE = (By.CSS_SELECTOR, ".moviename-big")
    FILM_ORIGINAL_TITLE = (By.CSS_SELECTOR, ".originalTitle")
    FILM_YEAR = (By.XPATH, "//td[contains(text(), 'год')]/following-sibling::td")
    FILM_RATING = (By.CSS_SELECTOR, ".rating_ball")
    FILM_RATING_COUNT = (By.CSS_SELECTOR, ".ratingCount")
    FILM_DESCRIPTION = (By.CSS_SELECTOR, ".brand_words[itemprop='description']")
    FILM_POSTER = (By.CSS_SELECTOR, ".popupBigImage img")
    FILM_TRAILER_BUTTON = (By.CSS_SELECTOR, ".trailer-button")
    FILM_ACTORS = (By.CSS_SELECTOR, ".actorList a")
    FILM_DIRECTOR = (By.XPATH, "//td[contains(text(), 'режиссер')]/following-sibling::td//a")
    FILM_GENRES = (By.XPATH, "//span[contains(@itemprop, 'genre')]")
    FILM_DURATION = (By.XPATH, "//td[contains(text(), 'время')]/following-sibling::td")

    @allure.step("Получить название фильма")
    def get_film_title(self) -> str:
        """Получить русское название фильма"""
        return self.get_text(self.FILM_TITLE)

    @allure.step("Получить оригинальное название фильма")
    def get_original_title(self) -> str:
        """Получить оригинальное название фильма"""
        if self.is_element_visible(self.FILM_ORIGINAL_TITLE):
            return self.get_text(self.FILM_ORIGINAL_TITLE)
        return ""

    @allure.step("Получить год выпуска фильма")
    def get_film_year(self) -> str:
        """Получить год выпуска фильма"""
        return self.get_text(self.FILM_YEAR)

    @allure.step("Получить рейтинг фильма")
    def get_film_rating(self) -> str:
        """Получить рейтинг фильма на Кинопоиске"""
        if self.is_element_visible(self.FILM_RATING):
            return self.get_text(self.FILM_RATING)
        return "Нет рейтинга"

    @allure.step("Получить количество оценок")
    def get_rating_count(self) -> str:
        """Получить количество оценок фильма"""
        if self.is_element_visible(self.FILM_RATING_COUNT):
            return self.get_text(self.FILM_RATING_COUNT)
        return ""

    @allure.step("Получить список актеров")
    def get_actors_list(self) -> list:
        """Получить список актеров фильма"""
        elements = self.find_elements(self.FILM_ACTORS)
        return [el.text for el in elements[:10]]  # Ограничим 10 актерами

    @allure.step("Получить жанры фильма")
    def get_film_genres(self) -> list:
        """Получить список жанров фильма"""
        elements = self.find_elements(self.FILM_GENRES)
        return [el.text for el in elements]

    @allure.step("Нажать кнопку трейлера")
    def click_trailer_button(self) -> None:
        """Нажать кнопку просмотра трейлера"""
        self.click(self.FILM_TRAILER_BUTTON)

    @allure.step("Проверить наличие постера")
    def is_poster_displayed(self) -> bool:
        """Проверить отображение постера фильма"""
        return self.is_element_visible(self.FILM_POSTER)
