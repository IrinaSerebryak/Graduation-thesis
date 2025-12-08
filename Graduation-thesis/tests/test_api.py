import pytest
import allure
from api.kinopoisk_api import KinopoiskAPI
from config.settings import settings
from config.test_data import TestData


@pytest.mark.api

class TestKinopoiskAPI:
    @pytest.fixture
    def api_client(self):
        """Фикстура для создания API клиента"""
        if not settings.API_KEY:
            pytest.skip("API ключ не установлен. Установите KINOPOISK_API_KEY в .env файле")
        return KinopoiskAPI()

    @allure.feature("API: Фильмы")
    @allure.story("Получение фильма по ID")
    @allure.title("Тест получения фильма по ID: {movie_id}")
    @pytest.mark.parametrize("movie_id", TestData.API_TEST_MOVIE_IDS[:3])
    def test_get_movie_by_id(self, api_client, movie_id):
        """Тест получения информации о фильме по ID"""
        with allure.step(f"Получить фильм с ID {movie_id}"):
            response = api_client.get_movie_by_id(movie_id)

        with allure.step("Проверить структуру ответа"):
            assert "id" in response
            assert response["id"] == movie_id
            assert "name" in response
            assert "year" in response
            assert "rating" in response

        with allure.step("Проверить данные фильма"):
            assert response["name"], "Название фильма не должно быть пустым"
            assert isinstance(response["year"], int), "Год должен быть числом"
            assert 1900 <= response["year"] <= 2100, "Некорректный год выпуска"

    @allure.feature("API: Поиск")
    @allure.story("Поиск фильмов по названию")
    @allure.title("Тест поиска фильма '{film_name}'")
    @pytest.mark.parametrize("film_name", TestData.TEST_FILMS[:2])
    def test_search_movies(self, api_client, film_name):
        """Тест поиска фильмов по названию"""
        with allure.step(f"Выполнить поиск фильма '{film_name}'"):
            response = api_client.search_movies(film_name, limit=5)

        with allure.step("Проверить структуру ответа"):
            assert "docs" in response
            assert "total" in response
            assert "page" in response
            assert "pages" in response

        with allure.step("Проверить результаты поиска"):
            assert response["total"] > 0, f"По запросу '{film_name}' ничего не найдено"
            assert len(response["docs"]) > 0, "Список фильмов пуст"

            # Проверить что найденные фильмы содержат искомое название
            found = False
            for movie in response["docs"]:
                if film_name.lower() in movie.get("name", "").lower():
                    found = True
                    break
            assert found, f"Фильм '{film_name}' не найден в результатах"

    @allure.feature("API: Фильтры")
    @allure.story("Поиск фильмов с фильтрами")
    @allure.title("Тест поиска фильмов с фильтром по году: {year}")
    @pytest.mark.parametrize("year", [2020, 2010, 2000])
    def test_search_movies_with_year_filter(self, api_client, year):
        """Тест поиска фильмов с фильтром по году"""
        with allure.step(f"Искать фильмы выпуска {year} года"):
            response = api_client.get_movies_with_filters(year=year, limit=5)

        with allure.step("Проверить что все фильмы соответствуют году"):
            for movie in response["docs"]:
                assert movie.get("year") == year, \
                    f"Фильм {movie.get('name')} имеет год {movie.get('year')}, ожидался {year}"

    @allure.feature("API: Фильтры")
    @allure.story("Поиск фильмов по рейтингу")
    @allure.title("Тест поиска фильмов с рейтингом выше {rating}")
    def test_search_movies_with_rating_filter(self, api_client):
        """Тест поиска фильмов с фильтром по рейтингу"""
        min_rating = 8.0

        with allure.step(f"Искать фильмы с рейтингом выше {min_rating}"):
            response = api_client.get_movies_with_filters(rating_kp=min_rating, limit=5)

        with allure.step("Проверить рейтинги фильмов"):
            for movie in response["docs"]:
                rating = movie.get("rating", {}).get("kp")
                if rating:
                    assert rating >= min_rating, \
                        f"Фильм {movie.get('name')} имеет рейтинг {rating}, ожидался >= {min_rating}"

    @allure.feature("API: Случайный фильм")
    @allure.story("Получение случайного фильма")
    @allure.title("Тест получения случайного фильма")
    def test_get_random_movie(self, api_client):
        """Тест получения случайного фильма"""
        with allure.step("Получить случайный фильм"):
            response = api_client.get_random_movie()

        with allure.step("Проверить структуру ответа"):
            assert "id" in response
            assert "name" in response
            assert "year" in response
            assert "type" in response

        with allure.step("Проверить данные фильма"):
            assert response["name"], "Название не должно быть пустым"
            assert response["type"] in ["movie", "tv-series"], \
                f"Некорректный тип: {response['type']}"

    @allure.feature("API: Топ 250")
    @allure.story("Получение фильмов из Топ 250")
    @allure.title("Тест получения фильмов из Топ 250")
    def test_get_top250_movies(self, api_client):
        """Тест получения фильмов из Топ 250"""
        with allure.step("Получить первые 10 фильмов из Топ 250"):
            response = api_client.get_top250(limit=10)

        with allure.step("Проверить структуру ответа"):
            assert "docs" in response
            assert len(response["docs"]) > 0, "Список фильмов Топ 250 пуст"

        with allure.step("Проверить рейтинги фильмов в Топ 250"):
            for movie in response["docs"]:
                rating = movie.get("rating", {}).get("kp")
                if rating:
                    assert rating >= 7.0, \
                        f"Фильм {movie.get('name')} в Топ 250 имеет низкий рейтинг: {rating}"

    @allure.feature("API: Актеры")
    @allure.story("Получение актеров фильма")
    @allure.title("Тест получения актеров фильма")
    def test_get_movie_persons(self, api_client):
        """Тест получения актеров фильма"""
        movie_id = TestData.API_TEST_MOVIE_IDS[0]

        with allure.step(f"Получить актеров фильма с ID {movie_id}"):
            response = api_client.get_movie_persons(movie_id)

        with allure.step("Проверить наличие актеров"):
            assert "docs" in response
            assert len(response["docs"]) > 0, "Список актеров пуст"

        with allure.step("Найти актеров в списке"):
            actors = [person for person in response["docs"]
                      if person.get("enProfession") == "actor"]
            assert len(actors) > 0, "В фильме нет информации об актерах"

    @allure.feature("API: Сериалы")
    @allure.story("Получение информации о сезонах сериала")
    @allure.title("Тест получения сезонов сериала")
    def test_get_series_seasons(self, api_client):
        """Тест получения информации о сезонах сериала"""
        # Используем ID известного сериала (например, "Во все тяжкие")
        series_id = 3498

        with allure.step(f"Получить информацию о сезонах сериала с ID {series_id}"):
            response = api_client.get_series_seasons(series_id)

        with allure.step("Проверить структуру ответа"):
            assert "docs" in response
            # Некоторые сериалы могут не иметь информации о сезонах в API
            if len(response["docs"]) > 0:
                season = response["docs"][0]
                assert "movieId" in season
                assert "number" in season
                assert "episodes" in season