import argparse
import csv
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(description='Обработка файлов и отчетов')

    parser.add_argument('--files', nargs='+', help='Список файлов для обработки')
    parser.add_argument('--report', type=str, help='Тип отчета')

    return parser.parse_args()


def validate_files(filenames):
    """Проверка существования файлов"""

    for filename in filenames:

        if not Path(filename).exists():
            raise FileNotFoundError(f"Файл не найден: {filename}")

        if not filename.lower().endswith('.csv'):
            raise ValueError(f"Файл не является CSV: {filename}")


def read_csv(filenames):
    """Читает CSV файлы."""

    parsed_rows = []

    validate_files(filenames)

    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                parsed_rows.append(row)

    return parsed_rows
