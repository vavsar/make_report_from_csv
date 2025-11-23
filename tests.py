import pytest

from helpers import validate_files
from main import parse_arguments, ReportCreator, PerformanceReport, read_csv
from unittest.mock import patch


class TestParseArguments:
    """Тесты для функции parse_arguments."""

    def test_parse_arguments_with_files_and_report(self):
        with patch('sys.argv', ['script.py', '--files', 'file1.csv', 'file2.csv', '--report', 'performance']):
            args = parse_arguments()
            assert args.files == ['file1.csv', 'file2.csv']
            assert args.report == 'performance'

    def test_parse_arguments_without_files(self):
        with patch('sys.argv', ['script.py', '--report', 'performance']):
            args = parse_arguments()
            assert args.files is None
            assert args.report == 'performance'

    def test_parse_arguments_without_report(self):
        with patch('sys.argv', ['script.py', '--files', 'file1.csv']):
            args = parse_arguments()
            assert args.files == ['file1.csv']
            assert args.report is None


class TestValidateFiles:
    """Тесты для функции validate_files"""

    def test_validate_files_with_existing_csv(self, tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nJohn,30")

        validate_files([str(csv_file)])

    def test_validate_files_with_nonexistent_file(self):
        with pytest.raises(FileNotFoundError, match="Файл не найден: nonexistent.csv"):
            validate_files(['nonexistent.csv'])

    def test_validate_files_with_non_csv_file(self, tmp_path):
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("some text")

        with pytest.raises(ValueError, match="Файл не является CSV: .*test.txt"):
            validate_files([str(txt_file)])


class TestReadCSV:
    """Тесты для функции read_csv"""

    def test_read_csv_single_file(self, tmp_path):
        # Создаем временный CSV файл
        csv_file = tmp_path / "test.csv"
        csv_content = """
            name,age,position,performance
            John,30,Developer,95
            Jane,25,Manager,88
        """
        csv_file.write_text(csv_content)

        result = read_csv([str(csv_file)])

        assert len(result) == 2
        assert result[0] == {'name': 'John', 'age': '30', 'position': 'Developer', 'performance': '95'}
        assert result[1] == {'name': 'Jane', 'age': '25', 'position': 'Manager', 'performance': '88'}

    def test_read_csv_multiple_files(self, tmp_path):
        # Создаем несколько временных CSV файлов
        csv_file1 = tmp_path / "test1.csv"
        csv_file1.write_text("""name,position,performance
John,Developer,95""")

        csv_file2 = tmp_path / "test2.csv"
        csv_file2.write_text("""name,position,performance
Jane,Manager,88""")

        result = read_csv([str(csv_file1), str(csv_file2)])

        assert len(result) == 2
        assert result[0] == {'name': 'John', 'position': 'Developer', 'performance': '95'}
        assert result[1] == {'name': 'Jane', 'position': 'Manager', 'performance': '88'}

    def test_read_csv_empty_file(self, tmp_path):
        # Создаем пустой CSV файл (только заголовки)
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("name,position,performance")

        result = read_csv([str(csv_file)])

        assert len(result) == 0

    def test_read_csv_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            read_csv(['nonexistent.csv'])

    def test_read_csv_invalid_extension(self, tmp_path):
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("some text")

        with pytest.raises(ValueError):
            read_csv([str(txt_file)])


class TestPerformanceReport:
    """Тесты для класса PerformanceReport"""

    def setup_method(self):
        self.report = PerformanceReport()

    def test_validate_data_valid(self):
        valid_data = [
            {'position': 'Developer', 'performance': '95'},
            {'position': 'Manager', 'performance': '88'}
        ]

        # Не должно вызывать исключений
        self.report.validate_data(valid_data)

    def test_validate_data_empty(self):
        with pytest.raises(ValueError, match="Нет данных для отчета"):
            self.report.validate_data([])

    def test_validate_data_missing_performance(self):
        invalid_data = [
            {'position': 'Developer', 'performance': '95'},
            {'position': 'Manager'}  # отсутствует performance
        ]

        with pytest.raises(ValueError, match="Неверная структура данных для отчета производительности"):
            self.report.validate_data(invalid_data)

    def test_validate_data_missing_position(self):
        invalid_data = [
            {'position': 'Developer', 'performance': '95'},
            {'performance': '88'}  # отсутствует position
        ]

        with pytest.raises(ValueError, match="Неверная структура данных для отчета производительности"):
            self.report.validate_data(invalid_data)

    def test_generate_report_output(self, capsys):
        test_data = [
            {'position': 'Developer', 'performance': '95'},
            {'position': 'Manager', 'performance': '88'}
        ]

        self.report.generate_report(test_data)

        captured = capsys.readouterr()
        output = captured.out

        assert "№" in output
        assert "Должность" in output
        assert "Эффективность" in output
        assert "Developer" in output
        assert "95" in output
        assert "Manager" in output
        assert "88" in output

    def test_generate_report_empty_data(self, capsys):
        self.report.generate_report([])

        captured = capsys.readouterr()
        output = captured.out

        # Проверяем, что заголовки выводятся даже для пустых данных
        assert "№" in output
        assert "Должность" in output
        assert "Эффективность" in output


class TestReportCreator:
    """Тесты для класса ReportCreator"""

    def test_get_report_performance(self):
        report = ReportCreator.get_report('performance')
        assert isinstance(report, PerformanceReport)

    def test_get_report_invalid_type(self):
        with pytest.raises(ValueError, match='Тип отчета "invalid" не поддерживается'):
            ReportCreator.get_report('invalid')

    def test_get_report_available_types_message(self):
        try:
            ReportCreator.get_report('invalid')
        except ValueError as e:
            error_message = str(e)
            assert 'performance' in error_message
            assert 'Доступные типы:' in error_message
