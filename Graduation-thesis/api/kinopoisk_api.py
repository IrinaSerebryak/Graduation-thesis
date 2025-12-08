import requests
import allure
from typing import Dict, Any, Optional
from config.settings import settings



class KinopoiskAPI:
    def __init__(self):
        self.base_url = settings.API_URL
        self.headers = {
            "X-API-KEY": settings.API_KEY,
            "Content-Type": "application/json"
        }

    @allure.step("Отправить GET запрос на {endpoint}")
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Базовый метод для отправки запросов"""
        url = f"{self.base_url}{endpoint}"
        kwargs['headers'] = self.headers
        return requests.request(method, url, **kwargs)

    @allure.step("Получить фильм по ID: {movie_id}")
    def get_movie_by_id(self, movie_id: int) -> Dict[str, Any]:
        """Получить информацию о фильме по ID"""
        response = self._request("GET", f"/movie/{movie_id}")
        response.raise_for_status()
        return response.json()

    @allure.step("Поиск фильмов по запросу: {query}")
    def search_movies(self, query: str, limit: int = 10, page: int = 1) -> Dict[str, Any]:
        """Поиск фильмов по названию"""
        params = {
            "query": query,
            "limit": limit,
            "page": page
        }
        response = self._request("GET", "/movie/search", params=params)
        response.raise_for_status()
        return response.json()

    @allure.step("Получить фильмы по фильтрам")
    def get_movies_with_filters(
            self,
            year: Optional[int] = None,
            rating_kp: Optional[float] = None,
            genre: Optional[str] = None,
            limit: int = 10
    ) -> Dict[str, Any]:
        """Получить фильмы с применением фильтров"""
        params = {"limit": limit}

        if year:
            params["year"] = year
        if rating_kp:
            params["rating.kp"] = rating_kp
        if genre:
            params["genres.name"] = genre

        response = self._request("GET", "/movie", params=params)
        response.raise_for_status()
        return response.json()

    @allure.step("Получить случайный фильм")
    def get_random_movie(self) -> Dict[str, Any]:
        """Получить случайный фильм"""
        response = self._request("GET", "/movie/random")
        response.raise_for_status()
        return response.json()

    @allure.step("Получить фильмы из Топ 250")
    def get_top250(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Получить фильмы из Топ 250"""
        params = {
            "lists": "top250",
            "page": page,
            "limit": limit
        }
        response = self._request("GET", "/movie", params=params)
        response.raise_for_status()
        return response.json()

    @allure.step("Получить сезоны и серии по ID сериала: {series_id}")
    def get_series_seasons(self, series_id: int) -> Dict[str, Any]:
        """Получить информацию о сезонах и сериях"""
        response = self._request("GET", f"/season?movieId={series_id}")
        response.raise_for_status()
        return response.json()

    @allure.step("Получить актеров по ID фильма: {movie_id}")
    def get_movie_persons(self, movie_id: int) -> Dict[str, Any]:
        """Получить актеров и съемочную группу фильма"""
        response = self._request("GET", f"/person?movieId={movie_id}")
        response.raise_for_status()
        return response.json()