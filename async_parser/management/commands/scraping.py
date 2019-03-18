from django.core.management.base import BaseCommand
from async_parser.models import ParserTask, TaskFile
from provernalog.models import City
from django.conf import settings
from async_parser.tasks import add_parcel
from zipfile import is_zipfile, ZipFile
import os


class PathDoesNotExist(Exception):
    pass


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.arguments = {}
        self.excel_arguments = {}
        self.files = []
        self.task = None
        super().__init__(*args, **kwargs)

    def get_arguments(self):
        self.arguments['path'] = input('Введите путь до папки или до файла: ')
        if not self.arguments['path']:
            raise ValueError
        self.arguments['region'] = int(input('Номер региона: '))
        self.arguments['group_type'] = input('Признак группы оценки (ZU/OKS): ')
        self.arguments['date_relevance'] = input('Дата актуальности (YYYY-MM-DD): ')
        is_excel = input('Добавить excel файлы? [y/N]: ')
        if is_excel.lower() == 'y':
            self.excel_arguments['cadastral_number'] = input("Название столбца с кадастровым номером: ")
            self.excel_arguments["group_appraise"] = input("Название столбца с группой оценки: ")
            self.excel_arguments["current_cost"] = input("Название столбца с текущей стоимостью: ")
            self.excel_arguments["cost_intermediate"] = input("Название столбца с промежуточной ценой: ")
            self.excel_arguments["approved_cost"] = input("Название столбца с утержденной стоимостью: ")
            self.excel_arguments["area"] = input("Название столбца с площадью: ")
            self.excel_arguments["address"] = input("Название столбца с местонахождением: ")
            self.excel_arguments["bydoc"] = input("Название столбца разрешенное использование: ")
            self.excel_arguments["date_relevance"] = input("Дата актуальности: ")

    def extract_zip(self, path):
        if is_zipfile(path):
            zip_file = ZipFile(path)
            try:
                full_path = os.path.splitext(path)[0]
                zip_file.extractall(path=full_path)
                os.remove(path)
                return full_path
            finally:
                zip_file.close()

    def path_preparation(self):
        _path = self.arguments['path']
        if os.path.exists(_path):
            if is_zipfile(_path) and _path.split('.')[-1].lower() == 'zip':
                _path = self.extract_zip(_path)
            if os.path.isfile(_path):
                self.files.append(os.path.abspath(_path))
            for rootdir, dirs, files in os.walk(_path):
                for file in files:
                    if file.split(".")[-1] in ["xml", "xlsx"]:
                        self.files.append(os.path.join(rootdir, file))
            self.arguments['path'] = _path
        else:
            raise PathDoesNotExist

    def task_register(self):
        self.task = ParserTask.objects.create(path=self.arguments['path'],
                                              city=City.objects.get(region=self.arguments['region']),
                                              group_type=self.arguments['group_type'].upper(),
                                              date_relevance=self.arguments['date_relevance'] or None)
        return self.task

    def create_task(self):
        for file in self.files:
            task_file = TaskFile.objects.create(task=self.task, path=file)
            task_args = {'file': file, 'task_file_id': self.task.id, 'region': self.arguments['region'],
                         'group_type': self.arguments['group_type'], 'date_relevance': self.arguments['date_relevance'],
                         'excel_name': self.excel_arguments}
            if settings.DEBUG:
                add_parcel(**task_args)
            else:
                celery_task = add_parcel.delay(**task_args)
                task_file.celery_id = celery_task.id
                task_file.save()

    def confirmation(self):
        print(f'''
                ==========================================================================================
                Количество файлов: {len(self.files)}
                Регион объектов: {self.arguments['region']}
                Признак группы: {self.arguments['group_type']}
                Дата актуальности: {self.arguments['date_relevance']}
                ==========================================================================================
                ''')
        accept = input('Начать загрузку объектов? [y/n]: ').lower()
        if accept == 'y' or accept == 'yes':
            return True
        else:
            return False

    def handle(self, *args, **kwargs):
        self.get_arguments()
        self.path_preparation()
        if self.confirmation():
            self.task_register()
            self.create_task()
        else:
            print('Abort.')
