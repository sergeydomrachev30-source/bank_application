import functools
import os
from typing import Any, Callable, Optional


def log(
    filename: Optional[str] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования выполнения функции.
    :param filename: Имя файла, в который будет записываться лог. Если None, лог выводится в консоль.
    :return: Функция-декоратор.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Пытаемся выполнить функцию
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"

                # Записываем успешный лог
                if filename is None:
                    print(log_message)
                else:
                    if os.path.dirname(filename):
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                return result

            except Exception as e:
                # Перехватываем ошибку и формируем детальное сообщение по ТЗ
                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                # Записываем лог ошибки перед тем, как пробросить её дальше
                if filename is None:
                    print(log_message)
                else:
                    if os.path.dirname(filename):
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")
                # Повторно выбрасываем исключение, чтобы не нарушать логику программы
                raise

        return wrapper

    return decorator
