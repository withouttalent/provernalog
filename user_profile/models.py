from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Report(models.Model):
    city = models.ForeignKey("provernalog.City", on_delete=models.CASCADE)
    title = models.CharField(_("Заголовок"), max_length=360)
    text = models.TextField(_("Текст отчета"))
    date_added = models.DateField(_("Дата добавления"))

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        ordering = ("-date_added",)


class SourceReport(models.Model):
    region = models.ForeignKey("provernalog.City", on_delete=models.CASCADE)
    title = models.CharField(max_length=360)
    date_relevance = models.DateField()

    class Meta:
        verbose_name = _("Перечень")
        verbose_name_plural = _("Перечень")
        ordering = ("region__region",)