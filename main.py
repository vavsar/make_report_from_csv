from abc import ABC, abstractmethod

from helpers import parse_arguments, read_csv


class BaseReport(ABC):
    """Абстрактный базовый класс для отчетов."""

    @abstractmethod
    def generate_report(self, data):
        pass

    @abstractmethod
    def validate_data(self, data):
        pass


class PerformanceReport:

    def validate_data(self, data):
        """Валидирует данные для отчета."""

        if not data:
            raise ValueError("Нет данных для отчета")

        for row in data:

            if 'performance' not in row or 'position' not in row:
                raise ValueError("Неверная структура данных для отчета производительности")

    def generate_report(self, data):
        """Генерирует отчет."""

        print(f"{'№':<5} | {'Должность':<20} | {'Эффективность':<15}")
        print("-" * 45)

        for i, row in enumerate(data, 1):
            position = row['position']
            performance = row['performance']
            print(f"{i:<5} | {position:<20} | {performance:<15}")


class ReportCreator:
    """Фабрика для создания отчетов"""

    report_types = {
        'performance': PerformanceReport(),
    }

    @classmethod
    def get_report(cls, report_type):
        """Возвращает отчет по типу или ошибку с перечнем поддерживаемых отчетов."""

        if report_type not in cls.report_types:
            raise ValueError(
                f'Тип отчета "{report_type}" не поддерживается. '
                f'Доступные типы: {list(cls.report_types.keys())}'
            )

        return cls.report_types[report_type]


if __name__ == "__main__":
    args = parse_arguments()

    if args.files:
        try:
            data = read_csv(args.files)

            if args.report:
                report = ReportCreator.get_report(args.report)
                report.generate_report(data)

        except (FileNotFoundError, ValueError) as e:
            print(f"Ошибка: {e}")
