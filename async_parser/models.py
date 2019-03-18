from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class ParserTask(models.Model):
    group_type = (
        ("ZU", "Земельные участки"),
        ("OKS", "Объекты капитального строительства")
    )
    path = models.CharField(_("Путь"), max_length=320)
    date_created = models.DateTimeField(_('Дата создания'), default=timezone.now)
    city = models.ForeignKey('provernalog.City', on_delete=models.SET_NULL, verbose_name="Город", null=True)
    group_type = models.CharField(_('Тип группы'), choices=group_type, max_length=12, blank=True, null=True)
    date_relevance = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        db_table = 'parser-tasks'


class TaskFile(models.Model):
    task = models.ForeignKey('async_parser.ParserTask', on_delete=models.CASCADE, verbose_name="Задача",
                             blank=True, null=True)
    path = models.CharField(_('Путь'), max_length=960, blank=True, null=True)
    is_parsed = models.BooleanField(_('Загружен'), default=False)
    celery_id = models.CharField(_('ID задачи'), max_length=320, blank=True, null=True)
    date_parsed = models.DateTimeField(_('Дата парсинга'), blank=True, null=True)
    parsed_parcels = models.IntegerField(_("Количество загруженных объектов"), default=0, blank=True, null=True)
    parcels = models.IntegerField(_('Количество объектов'), blank=True, null=True)
    errors = models.TextField(_("Ошибки"), blank=True, null=True)

    class Meta:
        verbose_name = "Файл задачи"
        verbose_name_plural = "Файлы задачи"
        db_table = 'parser-files'
