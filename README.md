# Печать отчетов из файлов .csv

Для запуска:
- склонировать репозиторий
- создать виртуальное окружение python3 -m venv venv
- активировать виртуальное окружение . venv/bin/activate
- установить зависимости pip install -r requirements.txt
- Запустить файл python3 main.py --files employees1.csv employees2.csv --report performance

При необходимости добавить новый тип отчета:
- в main.py создать класс отчета, отнаследованный от BaseReport
- в фабрике отчетов ReportCreator добавить новый отчет в аттрибут класса report_types 'параметр строки': название класса()
- запустить main.py с параметром нового отчета

Тесты находятся в модуле tests.py

Для запуска тестов:
- pytest tests.py -v
