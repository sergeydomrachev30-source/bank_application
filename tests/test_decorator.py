import os

import pytest

from src.decorators import log


def test_log_console_success(capsys):
    """Тест: успешный вызов функции с логированием в консоль."""

    @log()
    def sample_func(a, b):
        return a + b

    assert sample_func(2, 3) == 5
    captured = capsys.readouterr()
    assert "sample_func ok" in captured.out


def test_log_console_error(capsys):
    """Тест: логирование ошибки в консоль при падении функции."""

    @log()
    def error_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        error_func()

    captured = capsys.readouterr()
    assert "error_func error: ValueError. Inputs: (), {}" in captured.out


def test_log_file_success():
    """Тест: успешная запись лога в указанный файл."""
    log_file = "logs/test_success.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    @log(filename=log_file)
    def file_func(x):
        return x * 2

    assert file_func(10) == 20
    assert os.path.exists(log_file)

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "file_func ok" in content

    if os.path.exists(log_file):
        os.remove(log_file)


def test_log_file_error():
    """Тест: запись лога ошибки в указанный файл."""
    log_file = "logs/test_error.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    @log(filename=log_file)
    def file_err_func():
        raise TypeError("Type mistake")

    with pytest.raises(TypeError):
        file_err_func()

    assert os.path.exists(log_file)

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "file_err_func error: TypeError" in content

    if os.path.exists(log_file):
        os.remove(log_file)
