import csv
import json
import logging
import os

# Настраиваем логгер для модуля конвертации
logger = logging.getLogger("csv_to_json")
logger.setLevel(logging.INFO)


def csv_to_json(csv_file_path: str, json_file_path: str) -> None:
    """
    Функция для преобразования файла в формате csv в файл формата json.
    Защищена от падения при отсутствии исходного файла.
    """
    if not os.path.exists(csv_file_path):
        logger.error(f"Исходный CSV-файл не найден по пути: {csv_file_path}")
        return

    try:
        with open(csv_file_path, newline="", encoding="utf-8") as csv_file:
            # Сначала пробуем стандартный разделитель банка (запятая),
            # если колонок не появилось — пробуем точку с запятой
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            data = [row for row in csv_reader]

            # Проверка: если DictReader прочитал всё в одну колонку, пробуем изменить разделитель
            if data and len(data[0].keys()) <= 1:
                csv_file.seek(0)  # Сбрасываем указатель чтения в начало файла
                csv_reader = csv.DictReader(csv_file, delimiter=";")
                data = [row for row in csv_reader]

        # Создаем директорию для целевого файла, если её не существует
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

        with open(json_file_path, mode="w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        logger.info(f"Конвертация завершена. Файл успешно сохранен в: {json_file_path}")

    except Exception as e:
        logger.error(f"Критическая ошибка при конвертации CSV в JSON: {e}")
