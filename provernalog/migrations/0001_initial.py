# Generated by Django 2.1.1 on 2018-09-07 09:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import provernalog.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.CharField(max_length=70, unique=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', provernalog.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EvaluativeFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_factor', models.CharField(blank=True, max_length=240, null=True, verbose_name='ID Factor')),
                ('name', models.CharField(blank=True, max_length=320, null=True, verbose_name='Название фактора')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание фактора')),
                ('region', models.IntegerField(blank=True, null=True, verbose_name='Регион фактора')),
                ('quantitative_dimension', models.CharField(blank=True, max_length=240, null=True, verbose_name='Размерность количественного фактора')),
            ],
            options={
                'verbose_name': 'Ценообразующий фактор',
                'verbose_name_plural': 'Ценообразующие факторы',
                'db_table': 'evaluative_factor',
            },
        ),
        migrations.CreateModel(
            name='Formula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True, null=True, verbose_name='Формула оценки')),
                ('group', models.CharField(blank=True, max_length=50, null=True, verbose_name='Группа оценки')),
            ],
            options={
                'verbose_name': 'Формула оценки',
                'verbose_name_plural': 'Формулы оценки',
                'db_table': 'formula',
            },
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('cadastral_number', models.CharField(max_length=24, primary_key=True, serialize=False, verbose_name='Кадастровый номер')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Адрес')),
                ('region', models.IntegerField(blank=True, null=True, verbose_name='Регион')),
                ('area', models.FloatField(blank=True, null=True, verbose_name='площадь квм')),
                ('bydoc', models.TextField(blank=True, null=True, verbose_name='ByDoc')),
                ('assignation', models.TextField(blank=True, null=True, verbose_name='Назначение')),
                ('current_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='Текущая стоимость')),
                ('current_specific_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='УПКС текущей стоимости')),
                ('cost_intermediate', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='Ожидаемая стоимость')),
                ('specific_cost_intermediate', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='УПКС ожидаемой стоимости')),
                ('approved_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Утвержденная стоимость')),
                ('approved_specififc_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='УПКС утвержденной стоимости')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата оценки')),
                ('date_inform', models.DateField(blank=True, null=True, verbose_name='Дата оспаривания')),
                ('date_new', models.DateField(blank=True, null=True, verbose_name='Дата следующей оценки')),
                ('kladr', models.CharField(blank=True, max_length=50, null=True, verbose_name='КЛАДР')),
                ('okato', models.CharField(blank=True, max_length=50, null=True, verbose_name='ОКАТО')),
                ('formula', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='provernalog.Formula')),
            ],
            options={
                'verbose_name': 'Земельный участок',
                'verbose_name_plural': 'Земельные участки',
                'db_table': 'parcel',
            },
        ),
        migrations.CreateModel(
            name='ValueFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualitative_value', models.CharField(blank=True, max_length=240, null=True, verbose_name='Значение качественного фактора')),
                ('evaluative_factor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='provernalog.EvaluativeFactor')),
                ('parcel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='provernalog.Parcel')),
            ],
            options={
                'db_table': 'value_factor',
            },
        ),
        migrations.AddField(
            model_name='evaluativefactor',
            name='parcel',
            field=models.ManyToManyField(blank=True, null=True, through='provernalog.ValueFactor', to='provernalog.Parcel'),
        ),
    ]
