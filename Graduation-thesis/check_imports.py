"""
Проверка импортов проекта
"""

import sys
import os

# Добавляем корень проекта в путь
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print(f"Python path: {sys.path}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Корень проекта: {project_root}")

print("\nПроверка импортов...")

try:
    from settings import settings

    print("✅ config.settings импортирован успешно")
    print(f"  BASE_URL: {settings.BASE_URL}")
except ImportError as e:
    print(f"❌ Ошибка импорта config.settings: {e}")
    print("Проверьте наличие файла config/settings.py")

    # Проверим структуру
    print("\nСодержимое папки config:")
    if os.path.exists("config"):
        for root, dirs, files in os.walk("config"):
            for file in files:
                print(f"  {os.path.join(root, file)}")
    else:
        print("  Папка config не существует!")

try:
    from config.test_data import TestData

    print("✅ config.test_data импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта config.test_data: {e}")

print("\nПроверка завершена.")