import pytest
import allure
import sys
import os

# Добавляем корень проекта в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.kinopoisk_api import KinopoiskAPI
from config.settings import settings
from config.test_data import TestData


@pytest.mark.api
@allure.feature("API Тесты Кинопоиска")
class TestKinopoiskAPI:
    """Тесты API Кинопоиска"""

    @pytest.fixture
    def api_client(self):
        """Фикстура для создания API клиента"""
        if not settings.API_KEY or settings.API_KEY == "ваш_ключ_здесь":
            pytest.skip("API ключ не установлен. Установите KINOPOISK_API_KEY в .env файле")
        return KinopoiskAPI()

    @allure.story("Получение информации о фильмах")
    @allure.title("Тест получения фильма по ID")
    @pytest.mark.parametrize("movie_id", TestData.API_TEST_MOVIE_IDS[:3])
    def test_get_movie_by_id(self, api_client, movie_id):
        """Тест получения информации о фильме по ID"""
        with allure.step(f"Запрашиваем фильм с ID {movie_id}"):
            response = api_client.get_movie_by_id(movie_id)

        with allure.step("Проверяем структуру ответа"):
            assert "id" in response, "В ответе отсутствует поле 'id'"
            assert response[
                       "id"] == movie_id, f"ID фильма не совпадает: ожидалось {movie_id}, получено {response.get('id')}"
            assert "name" in response, "В ответе отсутствует поле 'name'"
            assert "year" in response, "В ответе отсутствует поле 'year'"
            assert "rating" in response, "В ответе отсутствует поле 'rating'"

        with allure.step("Проверяем данные фильма"):
            assert response["name"], "Название фильма не должно быть пустым"
            assert isinstance(response["year"], int), "Год должен быть числом"
            assert 1888 <= response["year"] <= 2100, f"Некорректный год выпуска: {response['year']}"

            allure.attach(
                f"Фильм: {response.get('name', 'N/A')}\n"
                f"Год: {response.get('year', 'N/A')}\n"
                f"Рейтинг: {response.get('rating', {}).get('kp', 'N/A')}",
                name="Информация о фильме"
            )

    @allure.story("Поиск фильмов")
    @allure.title("Тест поиска фильма '{film_name}'")
    @pytest.mark.parametrize("film_name", TestData.TEST_FILMS[:2])
    def test_search_movies(self, api_client, film_name):
        """Тест поиска фильмов по названию"""
        with allure.step(f"Ищем фильм '{film_name}'"):
            response = api_client.search_movies(film_name, limit=5)

        with allure.step("Проверяем структуру ответа"):
            assert "docs" in response, "В ответе отсутствует поле 'docs'"
            assert "total" in response, "В ответе отсутствует поле 'total'"
            assert "page" in response, "В ответе отсутствует поле 'page'"
            assert "pages" in response, "В ответе отсутствует поле 'pages'"

        with allure.step("Проверяем результаты поиска"):
            assert response["total"] > 0, f"По запросу '{film_name}' ничего не найдено"
            assert len(response["docs"]) > 0, "Список фильмов пуст"

            # Проверяем что найденные фильмы содержат искомое название
            found = False
            for movie in response["docs"][:5]:  # Проверяем первые 5 результатов
                movie_name = movie.get("name", "").lower()
                alternative_name = movie.get("alternativeName", "").lower()
                if film_name.lower() in movie_name or film_name.lower() in alternative_name:
                    found = True
                    break

            if not found:
                allure.attach(
                    f"Фильмы в результатах: {[m.get('name') for m in response['docs'][:3]]}",
                    name="Первые результаты поиска"
                )

            assert found, f"Фильм '{film_name}' не найден в первых результатах"

    @allure.story("Фильтрация фильмов")
    @allure.title("Тест фильтрации фильмов по году: {year}")
    @pytest.mark.parametrize("year", [2020, 2019, 2018])
    def test_search_movies_with_year_filter(self, api_client, year):
        """Тест поиска фильмов с фильтром по году"""
        with allure.step(f"Ищем фильмы {year} года"):
            response = api_client.get_movies_with_filters(year=year, limit=5)

        with allure.step("Проверяем что фильмы соответствуют году"):
            if response["docs"]:
                for movie in response["docs"]:
                    movie_year = movie.get("year")
                    if movie_year:
                        assert movie_year == year, \
                            f"Фильм '{movie.get('name')}' имеет год {movie_year}, ожидался {year}"

            allure.attach(
                f"Найдено фильмов: {len(response['docs'])}\n"
                f"Первый фильм: {response['docs'][0].get('name') if response['docs'] else 'Нет результатов'}",
                name="Результаты фильтрации"
            )

    @allure.story("Фильтрация по рейтингу")
    @allure.title("Тест фильтрации фильмов с рейтингом выше 8.0")
    def test_search_movies_with_rating_filter(self, api_client):
        """Тест поиска фильмов с фильтром по рейтингу"""
        min_rating = 8.0

        with allure.step(f"Ищем фильмы с рейтингом выше {min_rating}"):
            response = api_client.get_movies_with_filters(rating_kp=min_rating, limit=5)

        with allure.step("Проверяем рейтинги фильмов"):
            if response["docs"]:
                for movie in response["docs"]:
                    rating = movie.get("rating", {}).get("kp")
                    if rating:
                        assert rating >= min_rating, \
                            f"Фильм '{movie.get('name')}' имеет рейтинг {rating}, ожидался >= {min_rating}"

            allure.attach(
                f"Найдено фильмов с рейтингом > {min_rating}: {len(response['docs'])}",
                name="Результаты фильтрации по рейтингу"
            )

    @allure.story("Случайный фильм")
    @allure.title("Тест получения случайного фильма")
    def test_get_random_movie(self, api_client):
        """Тест получения случайного фильма"""
        with allure.step("Запрашиваем случайный фильм"):
            response = api_client.get_random_movie()

        with allure.step("Проверяем структуру ответа"):
            assert "id" in response, "В ответе отсутствует поле 'id'"
            assert "name" in response, "В ответе отсутствует поле 'name'"
            assert "year" in response, "В ответе отсутствует поле 'year'"
            assert "type" in response, "В ответе отсутствует поле 'type'"

        with allure.step("Проверяем данные фильма"):
            assert response["name"], "Название не должно быть пустым"
            assert response["type"] in ["movie", "tv-series", "cartoon", "anime"], \
                f"Некорректный тип: {response['type']}"

            allure.attach(
                f"Случайный фильм: {response.get('name')}\n"
                f"Тип: {response.get('type')}\n"
                f"Год: {response.get('year')}",
                name="Информация о случайном фильме"
            )

    @allure.story("Топ 250 фильмов")
    @allure.title("Тест получения фильмов из Топ 250")
    def test_get_top250_movies(self, api_client):
        """Тест получения фильмов из Топ 250"""
        with allure.step("Запрашиваем первые 10 фильмов из Топ 250"):
            response = api_client.get_top250(limit=10)

        with allure.step("Проверяем структуру ответа"):
            assert "docs" in response, "В ответе отсутствует поле 'docs'"
            assert len(response["docs"]) > 0, "Список фильмов Топ 250 пуст"

        with allure.step("Проверяем рейтинги фильмов в Топ 250"):
            high_rated_count = 0
            for movie in response["docs"]:
                rating = movie.get("rating", {}).get("kp")
                if rating and rating >= 7.0:
                    high_rated_count += 1

            assert high_rated_count > 0, "В Топ 250 должны быть фильмы с рейтингом >= 7.0"

            allure.attach(
                f"Всего фильмов: {len(response['docs'])}\n"
                f"С рейтингом >= 7.0: {high_rated_count}\n"
                f"Первый фильм: {response['docs'][0].get('name')}",
                name="Статистика Топ 250"
            )

    @allure.story("Актеры и съемочная группа")
    @allure.title("Тест получения актеров фильма")
    def test_get_movie_persons(self, api_client):
        """Тест получения актеров фильма"""
        movie_id = TestData.API_TEST_MOVIE_IDS[0]  # Зеленая миля

        with allure.step(f"Запрашиваем актеров фильма с ID {movie_id}"):
            response = api_client.get_movie_persons(movie_id)

        with allure.step("Проверяем наличие актеров"):
            assert "docs" in response, "В ответе отсутствует поле 'docs'"
            assert len(response["docs"]) > 0, "Список актеров пуст"

        with allure.step("Находим актеров в списке"):
            actors = [person for person in response["docs"]
                      if person.get("enProfession") == "actor"]

            assert len(actors) > 0, "В фильме нет информации об актерах"

            allure.attach(
                f"Всего персон: {len(response['docs'])}\n"
                f"Актеров: {len(actors)}\n"
                f"Первые 3 актера: {[a.get('name') for a in actors[:3]]}",
                name="Информация об актерах"
            )

    @allure.story("Сериалы")
    @allure.title("Тест получения информации о сезонах сериала")
    def test_get_series_seasons(self, api_client):
        """Тест получения информации о сезонах сериала"""
        series_id = 3498  # "Во все тяжкие"

        with allure.step(f"Запрашиваем информацию о сезонах сериала с ID {series_id}"):
            response = api_client.get_series_seasons(series_id)

        with allure.step("Проверяем структуру ответа"):
            assert "docs" in response, "В ответе отсутствует поле 'docs'"

            # Некоторые сериалы могут не иметь информации о сезонах в API
            if len(response["docs"]) > 0:
                season = response["docs"][0]
                assert "movieId" in season, "В сезоне отсутствует поле 'movieId'"
                assert "number" in season, "В сезоне отсутствует поле 'number'"
                assert "episodes" in season, "В сезоне отсутствует поле 'episodes'"

                allure.attach(
                    f"Найдено сезонов: {len(response['docs'])}\n"
                    f"Первый сезон: номер {season.get('number')}, эпизодов: {len(season.get('episodes', []))}",
                    name="Информация о сезонах"
                )
            else:
                allure.attach("Сериал не имеет информации о сезонах в API",
                              name="Нет данных о сезонах")

    @allure.story("Рецензии")
    @allure.title("Тест получения рецензий к фильму")
    def test_get_movie_reviews(self, api_client):
        """Тест получения рецензий к фильму"""
        movie_id = TestData.API_TEST_MOVIE_IDS[1]  # Побег из Шоушенка

        with allure.step(f"Запрашиваем рецензии к фильму с ID {movie_id}"):
            response = api_client.get_movie_reviews(movie_id, limit=5)

        with allure.step("Проверяем структуру ответа"):
            assert "docs" in response, "В ответе отсутствует поле 'docs'"

            if len(response["docs"]) > 0:
                review = response["docs"][0]
                assert "title" in review, "В рецензии отсутствует поле 'title'"
                assert "review" in review, "В рецензии отсутствует поле 'review'"

                allure.attach(
                    f"Найдено рецензий: {len(response['docs'])}\n"
                    f"Первая рецензия: {review.get('title')[:50]}...",
                    name="Информация о рецензиях"
                )
            else:
                allure.attach("Фильм не имеет рецензий в API",
                              name="Нет данных о рецензиях")

    @allure.story("Похожие фильмы")
    @allure.title("Тест получения похожих фильмов")
    def test_get_similar_movies(self, api_client):
        """Тест получения похожих фильмов"""
        movie_id = TestData.API_TEST_MOVIE_IDS[2]  # Начало

        with allure.step(f"Запрашиваем похожие фильмы для ID {movie_id}"):
            response = api_client.get_similar_movies(movie_id, limit=5)

        with allure.step("Проверяем наличие похожих фильмов"):
            assert "docs" in response, "В ответе отсутствует поле 'docs'"

            if len(response["docs"]) > 0:
                similar_movie = response["docs"][0]
                assert "id" in similar_movie, "В фильме отсутствует поле 'id'"
                assert "name" in similar_movie, "В фильме отсутствует поле 'name'"

                allure.attach(
                    f"Найдено похожих фильмов: {len(response['docs'])}\n"
                    f"Первый похожий фильм: {similar_movie.get('name')}",
                    name="Информация о похожих фильмах"
                )
            else:
                allure.attach("Фильм не имеет похожих фильмов в API",
                              name="Нет данных о похожих фильмах")