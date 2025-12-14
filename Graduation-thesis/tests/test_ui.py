import pytest
import allure
import sys
import os
import time

# Добавляем корень проекта в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from pages.search_page import SearchPage
from pages.login_page import LoginPage
from config.settings import settings
from config.test_data import TestData


@allure.feature("UI Тесты приложения")
@pytest.mark.ui
class TestKinopoiskUI:
    """UI тесты для сайта приложения"""

    def __init__(self):
        # Запрещаем ручное создание экземпляра и устраняем предупреждение IDE
        pass

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Настройка и очистка для каждого UI теста"""
        # Создаем папку для скриншотов если её нет
        os.makedirs("allure-results", exist_ok=True)

        # Настраиваем Chrome
        chrome_options = Options()

        if settings.HEADLESS:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Меняем user-agent
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        # Инициализируем драйвер
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        # Скрываем факт автоматизации
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        self.driver.implicitly_wait(settings.IMPLICITLY_WAIT)

        yield

        # Закрываем браузер после теста
        if hasattr(self, 'driver'):
            self.driver.quit()

    @allure.story("Главная страница")
    @allure.title("Тест открытия главной страницы")
    def test_open_main_page(self):
        """Тест открытия главной страницы приложения"""
        main_page = MainPage(self.driver)

        with allure.step("Открываем главную страницу приложения"):
            main_page.open(settings.BASE_URL)
            time.sleep(2)

        with allure.step("Проверяем наличие логотипа"):
            assert main_page.is_logo_visible(), "Логотип не отображается"
            allure.attach("Логотип отображается корректно", name="Логотип")

        with allure.step("Проверяем наличие поля поиска"):
            placeholder = main_page.get_search_placeholder()
            assert placeholder, "Поле поиска не имеет placeholder"
            allure.attach(f"Placeholder поля поиска: {placeholder}", name="Placeholder")

        with allure.step("Проверяем заголовок страницы"):
            title = self.driver.title
            assert "Кинопоиск" in title, f"Заголовок не содержит 'Кинопоиск': {title}"
            allure.attach(f"Заголовок страницы: {title}", name="Page Title")

        with allure.step("Делаем скриншот главной страницы"):
            screenshot_path = main_page.take_screenshot("main_page")
            allure.attach.file(screenshot_path, name="Главная страница",
                               attachment_type=allure.attachment_type.PNG)

    @allure.story("Поиск фильмов")
    @allure.title("Тест поиска фильма '{film_name}'")
    @pytest.mark.parametrize("film_name", TestData.TEST_FILMS[:3])
    def test_search_film(self, film_name):
        """Тест поиска фильма на сайте"""
        main_page = MainPage(self.driver)
        search_page = SearchPage(self.driver)

        with allure.step(f"Открываем главную страницу и ищем фильм '{film_name}'"):
            main_page.open(settings.BASE_URL)
            time.sleep(2)
            main_page.search(film_name)
            time.sleep(3)

        with allure.step("Проверяем результаты поиска"):
            results_count = search_page.get_results_count()
            allure.attach(f"Найдено результатов: {results_count}", name="Количество результатов")

            if results_count > 0:
                titles = search_page.get_result_titles()
                allure.attach(f"Найденные фильмы: {titles[:5]}", name="Результаты поиска")

                found = any(film_name.lower() in title.lower() for title in titles[:5])
                if not found:
                    allure.attach(f"Искали: {film_name}\nНашли: {titles[:3]}",
                                  name="Несоответствие поиска")
                assert found, f"Фильм '{film_name}' не найден в первых результатах"
            else:
                assert search_page.is_no_results_message_displayed(), \
                    "При отсутствии результатов должно отображаться соответствующее сообщение"

        with allure.step("Делаем скриншот результатов поиска"):
            search_page.take_screenshot(f"search_{film_name.replace(' ', '_')}")

    @allure.story("Навигация")
    @allure.title("Тест перехода на страницу фильма")
    def test_open_film_page(self):
        """Тест перехода на страницу конкретного фильма"""
        main_page = MainPage(self.driver)
        search_page = SearchPage(self.driver)

        test_film = TestData.TEST_FILMS[0]  # Интерстеллар

        with allure.step(f"Ищем фильм '{test_film}'"):
            main_page.open(settings.BASE_URL)
            time.sleep(2)
            main_page.search(test_film)
            time.sleep(3)

        with allure.step("Переходим на страницу первого найденного фильма"):
            search_page.go_to_film_by_index(0)
            time.sleep(3)

        with allure.step("Проверяем элементы страницы фильма"):
            current_url = self.driver.current_url
            assert "/film/" in current_url, f"Не перешли на страницу фильма. URL: {current_url}"

            page_source = self.driver.page_source.lower()
            assert test_film.lower() in page_source or "интерстеллар" in page_source, \
                f"Название фильма '{test_film}' не найдено на странице"
            assert "рейтинг" in page_source or "rating" in page_source, \
                "На странице фильма нет информации о рейтинге"

            allure.attach(f"URL страницы фильма: {current_url}", name="URL фильма")

        with allure.step("Делаем скриншот страницы фильма"):
            self.driver.save_screenshot("allure-results/film_page.png")

    @allure.story("Авторизация")
    @allure.title("Тест авторизации на сайте")
    def test_login(self):
        """Тест авторизации на сайте Кинопоиска"""
        main_page = MainPage(self.driver)
        login_page = LoginPage(self.driver)

        with allure.step("Переходим на страницу авторизации"):
            main_page.open(settings.BASE_URL)
            time.sleep(2)
            main_page.go_to_login()
            time.sleep(2)

        with allure.step("Вводим учетные данные"):
            login_page.login(settings.LOGIN, settings.PASSWORD)
            time.sleep(3)

        with allure.step("Проверяем успешность авторизации"):
            current_url = self.driver.current_url
            success = ("mykp" in current_url or "profile" in current_url or settings.BASE_URL in current_url)
            error_in_page = "ошибка" in self.driver.page_source.lower() or "error" in self.driver.page_source.lower()

            if not success or error_in_page:
                error_message = login_page.get_error_message()
                if error_message:
                    allure.attach(f"Сообщение об ошибке: {error_message}", name="Ошибка авторизации")
                allure.attach(f"URL: {current_url}", name="URL после авторизации")

            assert not error_in_page, "На странице обнаружена ошибка авторизации"

        with allure.step("Делаем скриншот после авторизации"):
            self.driver.save_screenshot("allure-results/after_login.png")

    @allure.story("Фильтрация")
    @allure.title("Тест фильтрации результатов поиска")
    def test_search_filters(self):
        """Тест применения фильтров поиска"""
        main_page = MainPage(self.driver)
        search_page = SearchPage(self.driver)

        with allure.step("Ищем фильмы жанра 'драма'"):
            main_page.open(settings.BASE_URL)
            time.sleep(2)
            main_page.search("драма")
            time.sleep(3)

        with allure.step("Применяем фильтр 'Только фильмы'"):
            if search_page.is_element_visible(search_page.FILM_TYPE_FILTER):
                search_page.apply_film_filter()
                time.sleep(2)

        with allure.step("Проверяем результаты после фильтрации"):
            results_count = search_page.get_results_count()
            assert results_count > 0, "После фильтрации не найдено результатов"
            allure.attach(f"Результатов после фильтрации: {results_count}", name="Результаты фильтрации")

        with allure.step("Делаем скриншот фильтров"):
            search_page.take_screenshot("search_with_filters")

    @allure.story("Контент страницы")
    @allure.title("Тест проверки контента страницы фильма")
    def test_film_page_content(self):
        """Тест проверки контента страницы фильма"""
        film_id = TestData.API_TEST_MOVIE_IDS[0]  # Зеленая миля

        with allure.step(f"Открываем страницу фильма с ID {film_id}"):
            self.driver.get(f"{settings.BASE_URL}/film/{film_id}/")
            time.sleep(3)

        with allure.step("Проверяем основные элементы страницы"):
            page_source = self.driver.page_source.lower()
            checks = [
                ("Название", "зеленая" in page_source or "green mile" in page_source),
                ("Год", "1999" in page_source),
                ("Жанры", "драма" in page_source),
                ("Актеры", "том хэнкс" in page_source or "hanks" in page_source),
                ("Описание", "описание" in page_source or "сюжет" in page_source),
            ]

            results = [f"{name}: {'✅' if ok else '❌'}" for name, ok in checks]
            present_count = sum(ok for _, ok in checks)

            allure.attach("\n".join(results), name="Проверка элементов страницы")
            assert present_count >= 3, f"Недостаточно элементов: {present_count}/5"

    @allure.story("Навигация по разделам")
    @allure.title("Тест перехода в раздел 'Топ 250'")
    def test_navigate_to_top250(self):
        """Тест навигации в раздел Топ 250"""
        main_page = MainPage(self.driver)

        with allure.step("Открываем главную страницу"):
            main_page.open(settings.BASE_URL)
            time.sleep(2)

        with allure.step("Переходим в раздел 'Топ 250'"):
            main_page.go_to_top250()
            time.sleep(3)

        with allure.step("Проверяем что перешли в нужный раздел"):
            current_url = self.driver.current_url.lower()
            page_title = self.driver.title.lower()
            assert "top" in current_url or "250" in current_url or "топ" in page_title, \
                f"Не в Топ 250: URL={current_url}, Title={page_title}"
            assert "фильм" in self.driver.page_source.lower(), "Нет списка фильмов"

    @allure.story("Формы")
    @allure.title("Тест работы формы поиска")
    def test_search_form_functionality(self):
        """Тест работы формы поиска"""
        main_page = MainPage(self.driver)

        with allure.step("Открываем главную страницу"):
            main_page.open(settings.BASE_URL)
            time.sleep(2)

        with allure.step("Проверяем поле поиска"):
            search_input = main_page.find_element(main_page.SEARCH_INPUT)
            test_text = "тест"

            search_input.send_keys(test_text)
            time.sleep(0.5)
            assert search_input.get_attribute("value") == test_text

            search_input.clear()
            time.sleep(0.5)
            assert search_input.get_attribute("value") == ""

            allure.attach("✅ Поле поиска: ввод и очистка работают", name="Проверка формы")

    @allure.story("Контент")
    @allure.title("Тест проверки основных элементов сайта")
    def test_site_elements(self):
        """Тест проверки основных элементов сайта"""
        main_page = MainPage(self.driver)

        with allure.step("Открываем главную страницу"):
            main_page.open(settings.BASE_URL)
            time.sleep(3)

        elements_to_check = [
            ("Логотип", main_page.is_logo_visible()),
            ("Поиск", main_page.is_element_visible(main_page.SEARCH_INPUT)),
            ("Кнопка входа", main_page.is_login_button_visible()),
        ]

        results = [f"{name}: {'✅' if ok else '❌'}" for name, ok in elements_to_check]
        visible_count = sum(ok for _, ok in elements_to_check)

        allure.attach("\n".join(results), name="Элементы интерфейса")
        assert visible_count >= 2, f"Мало элементов: {visible_count}/3"

        # Проверка контента
        body_text = self.driver.find_element("tag name", "body").text
        assert len(body_text) > 500, "Страница почти пустая"

    @allure.story("Негативные сценарии")
    @allure.title("Тест поиска несуществующего фильма")
    def test_search_nonexistent_film(self):
        """Тест поиска несуществующего фильма"""
        main_page = MainPage(self.driver)
        search_page = SearchPage(self.driver)

        invalid_query = "абвгдйклмнопрстуфхцчшщъыьэюя1234567890"

        with allure.step(f"Ищем несуществующий запрос: '{invalid_query}'"):
            main_page.open(settings.BASE_URL)
            time.sleep(2)
            main_page.search(invalid_query)
            time.sleep(3)

        with allure.step("Проверяем отсутствие результатов"):
            results_count = search_page.get_results_count()
            if results_count == 0:
                assert search_page.is_no_results_message_displayed(), \
                    "Должно быть сообщение 'ничего не найдено'"
                msg = search_page.get_no_results_message()
                allure.attach(f"Сообщение: {msg}", name="Результат поиска")
            else:
                allure.attach(f"Неожиданные результаты: {results_count}", name="⚠️ Неожиданные результаты")