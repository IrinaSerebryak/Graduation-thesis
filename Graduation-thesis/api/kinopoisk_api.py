import requests
import allure
import time
from typing import Dict, Any, Optional, List
from config.settings import settings


class KinopoiskAPI:
    """Клиент для работы с API Кинопоиска"""

    def __init__(self):
        self.base_url = settings.API_URL
        self.headers = {
            "X-API-KEY": "FQ1Y3JB-N9F43BE-PJ92X41-7BW07GB",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    @allure.step("Отправить запрос {method} на {endpoint}")
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Базовый метод для отправки запросов"""
        url = f"{self.base_url}{endpoint}"

        for attempt in range(settings.MAX_RETRIES):
            try:
                response = self.session.request(method, url, **kwargs)

                # Проверяем статус ответа
                if response.status_code == 429:
                    # Слишком много запросов - ждем и повторяем
                    wait_time = 2 ** attempt  # Экспоненциальная задержка
                    allure.attach(f"Получен 429 статус. Ожидание {wait_time} секунд...",
                                  name="Rate Limit")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                if attempt == settings.MAX_RETRIES - 1:
                    raise
                time.sleep(settings.RETRY_DELAY)

        raise requests.exceptions.RequestException("Не удалось выполнить запрос после нескольких попыток")

    @allure.step("Получить фильм по ID: {movie_id}")
    def get_movie_by_id(self, movie_id: int) -> Dict[str, Any]:
        """Получить информацию о фильме по ID"""
        response = self._make_request("GET", f"/movie/{movie_id}")
        return response.json()

    @allure.step("Поиск фильмов по запросу: '{query}'")
    def search_movies(self, query: str, limit: int = 10, page: int = 1) -> Dict[str, Any]:
        """Поиск фильмов по названию, актерам, режиссерам"""
        params = {
            "query": query,
            "limit": limit,
            "page": page
        }
        response = self._make_request("GET", "/movie/search", params=params)
        return response.json()

    @allure.step("Получить фильмы с фильтрами")
    def get_movies_with_filters(
            self,
            year: Optional[int] = None,
            rating_kp: Optional[float] = None,
            genre: Optional[str] = None,
            country: Optional[str] = None,
            limit: int = 10,
            page: int = 1
    ) -> Dict[str, Any]:
        """Получить фильмы с применением фильтров"""
        params = {
            "limit": limit,
            "page": page
        }

        if year:
            params["year"] = year
        if rating_kp:
            params["rating.kp"] = rating_kp
        if genre:
            params["genres.name"] = genre
        if country:
            params["countries.name"] = country

        response = self._make_request("GET", "/movie", params=params)
        return response.json()

    @allure.step("Получить случайный фильм")
    def get_random_movie(self) -> Dict[str, Any]:
        """Получить случайный фильм"""
        response = self._make_request("GET", "/movie/random")
        return response.json()

    @allure.step("Получить фильмы из Топ 250")
    def get_top250(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Получить фильмы из Топ 250 Кинопоиска"""
        params = {
            "lists": "top250",
            "page": page,
            "limit": limit
        }
        response = self._make_request("GET", "/movie", params=params)
        return response.json()

    @allure.step("Получить сезоны сериала по ID: {series_id}")
    def get_series_seasons(self, series_id: int) -> Dict[str, Any]:
        """Получить информацию о сезонах и сериях"""
        params = {"movieId": series_id}
        response = self._make_request("GET", "/season", params=params)
        return response.json()

    @allure.step("Получить актеров и съемочную группу фильма по ID: {movie_id}")
    def get_movie_persons(self, movie_id: int) -> Dict[str, Any]:
        """Получить актеров и съемочную группу фильма"""
        params = {"movieId": movie_id}
        response = self._make_request("GET", "/person", params=params)
        return response.json()

    @allure.step("Получить рецензии к фильму по ID: {movie_id}")
    def get_movie_reviews(self, movie_id: int, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Получить рецензии к фильму"""
        params = {
            "movieId": movie_id,
            "page": page,
            "limit": limit
        }
        response = self._make_request("GET", "/review", params=params)
        return response.json()

    @allure.step("Получить похожие фильмы по ID: {movie_id}")
    def get_similar_movies(self, movie_id: int, limit: int = 10) -> Dict[str, Any]:
        """Получить похожие фильмы"""
        params = {
            "movieId": movie_id,
            "limit": limit
        }
        response = self._make_request("GET", "/movie", params=params)
        return response.json()