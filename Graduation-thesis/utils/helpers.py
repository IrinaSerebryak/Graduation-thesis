import random
import string
import time
from typing import List, Dict, Any


def generate_random_string(length: int = 10) -> str:
    """Сгенерировать случайную строку заданной длины (только латинские буквы)"""
    letters = string.ascii_letters  # a-z, A-Z
    return ''.join(random.choice(letters) for _ in range(length))  # ← _ вместо i


def wait_for_condition(condition_func, timeout: int = 10, interval: float = 0.5) -> bool:
    """
    Ожидание выполнения условия в течение timeout секунд с интервалом проверки.

    :param condition_func: функция без аргументов, возвращающая bool
    :param timeout: максимальное время ожидания (сек)
    :param interval: интервал между проверками (сек)
    :return: True, если условие выполнилось; False — если таймаут
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    return False


def validate_film_data(film_data: Dict[str, Any]) -> List[str]:
    """
    Валидация данных фильма.

    :param film_data: словарь с данными фильма
    :return: список ошибок (пустой — если всё валидно)
    """
    errors = []

    # Обязательные поля
    required_fields = ["id", "name", "year", "type"]
    for field in required_fields:
        if field not in film_data:
            errors.append(f"Отсутствует обязательное поле: '{field}'")

    # Название не должно быть пустым
    if "name" in film_data and not film_data["name"]:
        errors.append("Название фильма не может быть пустым")

    # Проверка года
    if "year" in film_data:
        year = film_data["year"]
        if not isinstance(year, int):
            errors.append(f"Год должен быть целым числом, получено: {type(year).__name__}")
        elif year < 1888 or year > 2100:
            errors.append(f"Некорректный год: {year} (должен быть в диапазоне 1888–2100)")

    # Проверка рейтинга "Кинопоиска
    if "rating" in film_data and isinstance(film_data["rating"], dict):
        rating = film_data["rating"].get("kp")
        if rating is not None:
            if not isinstance(rating, (int, float)):
                errors.append(f"Рейтинг должен быть числом, получено: {type(rating).__name__}")
            elif rating < 0 or rating > 10:
                errors.append(f"Некорректный рейтинг КП: {rating} (должен быть от 0.0 до 10.0)")

    return errors