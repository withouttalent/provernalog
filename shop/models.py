from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
import uuid
# Create your models here.


class Product(models.Model):
    PAYMENT_SUBJECT = (
        ("commodity", "Товар"), ("excise", "Подакцизный товар"), ("job", "Работа"), ("service", "Услуга"),
        ("intellectual_activity", "Результаты интеллектуальной деятельности"), ("payment", "Платеж"),
        ("agent_commission", "Агентское вознаграждение"), ("composite", "Несколько вариантов"), ("another", "Другое"))
    PAYMENT_MODE = (
        ("full_prepayment", "Полная предоплата"), ("partial_prepayment", "Частичная предоплата"), ("advance", "Аванс"),
        ("full_payment", "Полный расчет")
    )
    title = models.CharField(_("Название"), max_length=780)
    subtitle = models.CharField(_("Название для чека"), max_length=128, blank=True, null=True)
    body = RichTextField(_("Описание товара"))
    image = models.ImageField(_("Картинка товара"), upload_to="shop/", blank=True, null=True)
    price = models.FloatField(_("Цена товара"))
    payment_subject = models.CharField(_("Признак предмета расчета"), choices=PAYMENT_SUBJECT, max_length=120,
                                       blank=True, null=True)
    payment_mode = models.CharField(_("Признак способа расчета"), choices=PAYMENT_MODE, max_length=120,
                                    blank=True, null=True)
    date_created = models.DateTimeField(_("Дата добавления"))

    def __str__(self):
        return self.title[:72]

    def chunk_body(self):
        return self.body[:240]

    class Meta:
        ordering = ("date_created",)
        db_table = 'products'
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


def get_default_as_uuid():
    return str(uuid.uuid4()).replace('-', '')


class Order(models.Model):
    STATUS = (
        ("processed", 'В процессе'),
        ("success", 'Успешно'),
        ("fail", 'Не оплачено'),
    )
    user = models.CharField(_("Данные покупателя"), max_length=240)
    parcel = models.ForeignKey('provernalog.Parcel', on_delete=models.SET_NULL, blank=True, null=True)
    inn = models.CharField(_("Инн"), max_length=20, blank=True, null=True)
    user_id = models.CharField(_("Уникальный номер пользователя"), max_length=62, default=get_default_as_uuid)
    phone = models.CharField(_("Номер телефона"), max_length=16)
    email = models.EmailField(_("Email покупателя"), max_length=120)
    status = models.CharField(choices=STATUS, max_length=45, blank=True, null=True)
    count = models.PositiveIntegerField(_("Количество товара"), default=1)
    payment_id = models.CharField(max_length=62, blank=True, null=True)
    amount = models.PositiveIntegerField(_("Сумма заказа"))
    good = models.ForeignKey("shop.Product", verbose_name="Товар", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        db_table = 'orders'
