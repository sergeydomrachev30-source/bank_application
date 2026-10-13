# tests/conftest.py
import os
import sys

# Автоматически добавляем папку src в пути поиска Python при запуске тестов
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
