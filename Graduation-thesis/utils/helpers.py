import random
import string
import time
from typing import List, Dict, Any


def generate_random_string(length: int = 10) -> str:
    """Сгенерировать случайную строку"""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def wait_for_condition(condition_func, timeout: int = 10, interval: float = 0.5) -> bool:
    """Ожидание выполнения условия"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    return False


def validate_film_data(film_data: Dict[str, Any]) -> List[str]:
    """Валидация данных фильма"""
    errors = []

    required_fields = ["id", "name", "year", "type"]
    for field in required_fields:
        if field not in film_data:
            errors.append(f"Отсутствует обязательное поле: {field}")

    if "name" in film_data and not film_data["name"]:
        errors.append("Название фильма не может быть пустым")

    if "year" in film_data:
        year = film_data["year"]
        if not isinstance(year, int):
            errors.append("Год должен быть числом")
        elif year < 1888 or year > 2100:  # Первый фильм был в 1888
            errors.append(f"Некорректный год: {year}")

    if "rating" in film_data and "kp" in film_data["rating"]:
        rating = film_data["rating"]["kp"]
        if rating is not None and (rating < 0 or rating > 10):
            errors.append(f"Некорректный рейтинг: {rating}")

    return errors