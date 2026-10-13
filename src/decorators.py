import functools
from typing import Any, Callable, Optional


def log(
    filename: Optional[str] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Декоратор для логирования выполнения функции.
        параметр filename: Имя файла, в который будет записываться
        лог. Если None, лог выводится в консоль.
        возвращает: Функция-декоратор.
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log_message = ""
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                return result
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                raise
            finally:
                if filename is None:
                    print(log_message)  # Убедись, что это вызывается
                else:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message + "\n")

        return wrapper

    return decorator
