import pytest

from src.decorators import log


def my_function(a, b):
    return a + b


# Тест успешного выполнения
@log(filename=None)
def test_successful_functioning():
    assert my_function(2, 3) == 5


# Тест обработки исключений
@log(filename=None)
def test_exception_functioning():
    with pytest.raises(TypeError):
        my_function(2, "a")


# # Тест вывода в консоль с использованием capsys
# @log(filename=None)
# def test_console_output_success(capsys):
#     result = my_function(2, 3)
#     captured = capsys.readouterr()
#     assert "my_function ok" in captured.out
#     assert result == 5
#
# @log(filename=None)
# def test_exception_function(capsys):
#     with pytest.raises(TypeError):
#         my_function(1, "a")
#     captured = capsys.readouterr()
#     assert "my_function error" in captured.out
