import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.film_page import FilmPage
from config.settings import settings
from config.test_data import TestData


@pytest.mark.api

class TestKinopoiskUI:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Фикстура для настройки драйвера"""
        chrome_options = Options()

        if settings.HEADLESS:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        # Меняем user-agent
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        self.driver.implicitly_wait(settings.TIMEOUT)

        yield

        self.driver.quit()

    @allure.feature("Главная страница")
    @allure.story("Открытие главной страницы")
    @allure.title("Тест открытия главной страницы Кинопоиска")


    def test_open_main_page(self):
        """Тест открытия главной страницы"""
        main_page = MainPage(self.driver)

        with allure.step("Открыть главную страницу Кинопоиска"):
            main_page.open(settings.BASE_URL)

        with allure.step("Проверить наличие логотипа"):
            assert main_page.is_logo_visible(), "Логотип не отображается"

        with allure.step("Проверить наличие поля поиска"):
            placeholder = main_page.get_search_placeholder()
            assert "фильм" in placeholder.lower(), "Поле поиска не содержит ожидаемый текст"

    @allure.feature("Поиск")
    @allure.story("Успешный поиск фильма")
    @allure.title("Тест поиска фильма '{film_name}'")
    @pytest.mark.parametrize("film_name", TestData.TEST_FILMS[:3])


    def test_search_film(self, film_name):
        """Тест поиска фильма"""
        main_page = MainPage(self.driver)
        search_page = SearchPage(self.driver)

        with allure.step(f"Открыть главную страницу и выполнить поиск фильма '{film_name}'"):
            main_page.open(settings.BASE_URL)
            main_page.search(film_name)

        with allure.step("Проверить результаты поиска"):
            results_count = search_page.get_results_count()
            assert results_count > 0, f"По запросу '{film_name}' не найдено результатов"

        with allure.step("Проверить наличие искомого фильма в результатах"):
            titles = search_page.get_result_titles()
            found = any(film_name.lower() in title.lower() for title in titles[:5])
            assert found, f"Фильм '{film_name}' не найден в первых результатах"

    @allure.feature("Поиск")
    @allure.story("Поиск несуществующего фильма")
    @allure.title("Тест поиска несуществующего фильма")


    def test_search_nonexistent_film(self):
        """Тест поиска несуществующего фильма"""
        main_page = MainPage(self.driver)
        search_page = SearchPage(self.driver)

        with allure.step("Открыть главную страницу и выполнить поиск случайной строки"):
            main_page.open(settings.BASE_URL)
            main_page.search("абвгдйклмнопрстуфхцчшщъыьэюя1234567890")

        with allure.step("Проверить сообщение об отсутствии результатов"):
            assert search_page.is_no_results_message_displayed(), \
                "Не отображается сообщение об отсутствии результатов"

    @allure.feature("Навигация")
    @allure.story("Переход к странице фильма")
    @allure.title("Тест перехода на страницу фильма из результатов поиска")


    def test_open_film_page_from_search(self):
        """Тест перехода на страницу фильма"""
        main_page = MainPage(self.driver)
        search_page = SearchPage(self.driver)
        film_page = FilmPage(self.driver)

        test_film = TestData.TEST_FILMS[0]

        with allure.step(f"Выполнить поиск фильма '{test_film}'"):
            main_page.open(settings.BASE_URL)
            main_page.search(test_film)

        with allure.step("Перейти на страницу первого найденного фильма"):
            search_page.go_to_film_by_index(0)

        with allure.step("Проверить элементы страницы фильма"):
            assert film_page.get_film_title(), "Название фильма не отображается"
            assert film_page.is_poster_displayed(), "Постер фильма не отображается"

            rating = film_page.get_film_rating()
            if rating != "Нет рейтинга":
                assert float(rating) > 0, "Рейтинг должен быть положительным"

    @allure.feature("Фильтрация")
    @allure.story("Применение фильтров поиска")
    @allure.title("Тест фильтрации результатов поиска")


    def test_search_filters(self):
        """Тест применения фильтров поиска"""
        main_page = MainPage(self.driver)
        search_page = SearchPage(self.driver)

        with allure.step("Выполнить поиск фильма 'драма'"):
            main_page.open(settings.BASE_URL)
            main_page.search("драма")

        with allure.step("Применить фильтр 'Только фильмы'"):
            search_page.apply_film_filter()

        with allure.step("Проверить наличие фильмов в результатах"):
            results_count = search_page.get_results_count()
            assert results_count > 0, "После фильтрации не найдено результатов"

    @allure.feature("Контент")
    @allure.story("Просмотр информации о фильме")
    @allure.title("Тест проверки информации на странице фильма")
    def test_film_page_content(self):
        """Тест проверки контента страницы фильма"""
        # Используем прямой переход к известному фильму
        film_page = FilmPage(self.driver)
        film_id = TestData.API_TEST_MOVIE_IDS[0]

        with allure.step(f"Открыть страницу фильма с ID {film_id}"):
            film_page.open(f"{settings.BASE_URL}/film/{film_id}/")

        with allure.step("Проверить основные элементы страницы"):
            title = film_page.get_film_title()
            assert title, "Название фильма не найдено"

            year = film_page.get_film_year()
            assert year.isdigit() and int(year) > 1900, f"Некорректный год: {year}"

            genres = film_page.get_film_genres()
            assert len(genres) > 0, "Жанры не указаны"

            actors = film_page.get_actors_list()
            assert len(actors) > 0, "Актеры не указаны"

    @allure.feature("Навигация")
    @allure.story("Переход в раздел Топ 250")
    @allure.title("Тест перехода в раздел Топ 250 фильмов")
    def test_navigate_to_top250(self):
        """Тест навигации в раздел Топ 250"""
        main_page = MainPage(self.driver)

        with allure.step("Открыть главную страницу"):
            main_page.open(settings.BASE_URL)

        with allure.step("Перейти в раздел Топ 250"):
            main_page.go_to_top250()

        with allure.step("Проверить URL раздела Топ 250"):
            assert "top" in self.driver.current_url, "Не перешли в раздел Топ 250"