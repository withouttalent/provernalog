# Generated by Django 2.1.2 on 2019-02-08 06:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('provernalog', '0019_auto_20190208_0648'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParserTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=320, verbose_name='Путь')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2019, 2, 8, 6, 48, 35, 976104, tzinfo=utc), verbose_name='Дата создания')),
                ('group_type', models.CharField(blank=True, choices=[('ZU', 'Земельные участки'), ('OKS', 'Объекты капитального строительства')], max_length=12, null=True, verbose_name='Тип группы')),
                ('date_relevance', models.DateField(blank=True, null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='provernalog.City', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'db_table': 'parser-tasks',
            },
        ),
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(blank=True, max_length=960, null=True, verbose_name='Путь')),
                ('is_parsed', models.BooleanField(default=False, verbose_name='Загружен')),
                ('celery_id', models.CharField(blank=True, max_length=320, null=True, verbose_name='ID задачи')),
                ('date_parsed', models.DateTimeField(blank=True, null=True, verbose_name='Дата парсинга')),
                ('parsed_parcels', models.IntegerField(blank=True, null=True, verbose_name='Количество загруженных объектов')),
                ('parcels', models.IntegerField(blank=True, null=True, verbose_name='Количество объектов')),
                ('errors', models.TextField(blank=True, null=True, verbose_name='Ошибки')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='async_parser.ParserTask', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Файл задачи',
                'verbose_name_plural': 'Файлы задачи',
                'db_table': 'parser-files',
            },
        ),
    ]
