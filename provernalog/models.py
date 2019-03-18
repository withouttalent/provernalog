from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal, ROUND_HALF_EVEN
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import uuid
from base64 import b64encode



class Parcel(models.Model):
    ASSIGNATION = (("005001001000", "Нежилое здание"),
        ("005001002000", "Жилой дом"),
        ("005001003000", "Многоквартирный дом"),
        ("005001999000", "Иное"),
        ("005002001000", "Жилое"),
        ("005002001001", "Комната"),
        ("005002001002", "Квартира"),
        ("005002002000", "Нежилое"),
        ("005002999000", "Иное"))
    cadastral_number = models.CharField(_("Кадастровый номер"), primary_key=True, max_length=24)
    address = models.TextField(_("Адрес"), blank=True, null=True)
    region = models.IntegerField(_("Регион"), blank=True, null=True)
    area = models.FloatField(_("площадь квм"), blank=True, null=True)
    bydoc = models.TextField(_("ByDoc"), blank=True, null=True)
    utilization = models.ForeignKey('Utilization', on_delete=models.CASCADE, blank=True, null=True)
    assignation = models.CharField(_("Назначение"), choices=ASSIGNATION, blank=True, max_length=61, null=True)
    current_cost = models.DecimalField(_("Текущая стоимость"), max_digits=21, decimal_places=2, blank=True, null=True)
    current_specific_cost = models.DecimalField(_("УПКС текущей стоимости"), max_digits=21, decimal_places=2,
                                                blank=True, null=True)
    cost_intermediate = models.DecimalField(_("Ожидаемая стоимость"), max_digits=21, decimal_places=2, blank=True,
                                            null=True)
    cost_pre_intermediate = ArrayField(models.DecimalField(max_digits=21, decimal_places=2), blank=True, null=True)
    specific_cost_intermediate = models.DecimalField(_("УПКС ожидаемой стоимости"), max_digits=21, decimal_places=2,
                                                     blank=True, null=True)
    specific_cost_pre_intermediate = ArrayField(models.DecimalField(max_digits=21, decimal_places=2), blank=True, null=True)
    approved_cost = models.DecimalField(_("Утвержденная стоимость"), max_digits=21, decimal_places=2, blank=True,
                                        null=True)
    approved_specififc_cost = models.DecimalField(_("УПКС утвержденной стоимости"), max_digits=21, decimal_places=2,
                                                  blank=True, null=True)
    group_appraise = models.ForeignKey("GroupAppraise", on_delete=models.CASCADE, blank=True, null=True)
    subgroup_appraise = models.ForeignKey("SubgroupAppraise", on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(_("Дата оценки"), auto_now=False, auto_now_add=False, blank=True, null=True)
    date_inform = models.DateField(_("Дата оспаривания"), auto_now=False, auto_now_add=False, blank=True, null=True)
    date_new = models.DateField(_("Дата следующей оценки"), auto_now=False, auto_now_add=False, blank=True, null=True)
    formula = models.ForeignKey("Formula", on_delete=models.CASCADE, blank=True, null=True)
    date_relevance = models.DateField(_("Дата актуальности"), auto_now=False, blank=True, null=True)

    class Meta:
        verbose_name = _("Земельный участок")
        verbose_name_plural = _("Земельные участки")
        db_table = "parcel"

    def percent_change(self, current, changed):
        if current and changed:
            return str(Decimal(100 * ((changed - current) / current)).__format__('.2f')) + " %"

    def spec_cost(self, current):
        if current and self.area:
            return str(Decimal(current / Decimal(str(self.area))).__format__('.2f')) + " руб."
        return None

    def factors(self):
        parcel_factor = self.valuefactor_set.all()
        factor = [f"{factor.evaluative_factor.name}: {factor.qualitative_value} {factor.evaluative_factor.quantitative_dimension}" for factor in parcel_factor]
        return factor


class Formula(models.Model):
    value = models.TextField(_("Формула оценки"), blank=True, null=True)
    group = models.CharField(_("Группа оценки"), max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _("Формула оценки")
        verbose_name_plural = _("Формулы оценки")
        db_table = "formula"

    def __str__(self):
        return self.value


class Utilization(models.Model):
    code = models.CharField(_("Код"), unique=True, max_length=50)
    name = models.TextField(_("Назначение"))

    def __str__(self):
        return self.name[:70]

    class Meta:
        verbose_name = _("Вид разрешенного использования")
        verbose_name_plural = _("Виды разрешенного использования")


# Ценообразующий фактор
class EvaluativeFactor(models.Model):
    parcel = models.ManyToManyField(Parcel, through="ValueFactor", blank=True)  # Связь на земельный участок
    id_factor = models.CharField(_("ID Factor"), max_length=240, blank=True, null=True)
    name = models.CharField(_("Название фактора"), max_length=320, blank=True, null=True)  # Name_Factor
    description = models.TextField(_("Описание фактора"), blank=True, null=True)  # Уточненное описание Name_Factor_Desc
    region = models.IntegerField(_("Регион фактора"), blank=True, null=True)
    quantitative_dimension = models.CharField(_("Размерность количественного фактора"), max_length=240,
                                              blank=True, null=True)

    def __str__(self):
        return self.id_factor



    class Meta:
        verbose_name = "Ценообразующий фактор"
        verbose_name_plural = "Ценообразующие факторы"
        db_table = "evaluative_factor"


class ValueFactor(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, blank=True, null=True)
    evaluative_factor = models.ForeignKey(EvaluativeFactor, on_delete=models.CASCADE, blank=True, null=True)
    qualitative_value = models.CharField(_("Значение качественного фактора"), max_length=240, blank=True, null=True)  # Как и булевское значение так и дробное значение be aware

    class Meta:
        db_table = "value_factor"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(_("Email"), unique=True, max_length=70)
    phone = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    first_name = models.CharField(_("Имя"), max_length=50, blank=True, null=True)
    last_name = models.CharField(_("Фамилия"), max_length=50, blank=True, null=True)
    patronymic = models.CharField(_("Отчество"), max_length=50, blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


def support_hash():
    _uuid = uuid.uuid4()
    hash = b64encode(str(_uuid).encode())
    return hash.decode()


class Support(models.Model):
    sender = models.CharField(_("Имя отправителя"), max_length=120)
    email = models.EmailField(_("Почта отправителя"), max_length=128, blank=True, null=True)
    phone = models.CharField(_("Номер отправителя"), max_length=128)
    cadastral_number = models.CharField(_("Кадастровый номер"), max_length=128)
    address = models.CharField(_("Адрес"), max_length=960, blank=True, null=True)
    hash = models.CharField(_('Hash'), default=support_hash, max_length=96, blank=True, null=True)
    is_close = models.BooleanField(_("Обращение закрыто"), default=False)

    def __str__(self):
        if self.sender:
            return self.sender
        else:
            return self.email

    class Meta:
        verbose_name = _("Обращение")
        verbose_name_plural = _("Обращения")
        db_table = "support"


class GroupAppraise(models.Model):
    group_id = models.IntegerField()
    name = models.CharField(max_length=240)
    region = models.IntegerField()
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=180)
    source_url = models.URLField(max_length=360, blank=True, null=True)
    file = models.FileField(upload_to='words/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        db_table = 'cities'
        ordering = ('region',)


class SubgroupAppraise(models.Model):
    group = models.ForeignKey(GroupAppraise, on_delete=models.CASCADE, blank=True, null=True)
    subgroup_id = models.IntegerField()
    name = models.CharField(max_length=240)

    def __str__(self):
        return self.name


class ParcelAggregate(Parcel):

    class Meta:
        proxy = True
        verbose_name = "Статистика Объекта"
        verbose_name_plural = "Статистика Объектов"


class ParcelStatic(Parcel):

    class Meta:
        proxy = True
        verbose_name = "Общая статистика"
        verbose_name_plural = "Общая статистика"
