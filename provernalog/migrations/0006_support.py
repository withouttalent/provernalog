# Generated by Django 2.1.1 on 2018-09-13 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provernalog', '0005_auto_20180907_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=120, verbose_name='Имя отправителя')),
                ('email', models.EmailField(blank=True, max_length=128, null=True, verbose_name='Почта отправителя')),
                ('phone', models.CharField(max_length=128, verbose_name='Номер отправителя')),
                ('cadastral_number', models.CharField(max_length=128, verbose_name='Кадастровый номер')),
                ('is_close', models.BooleanField(default=False, verbose_name='Обращение закрыто')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
                'db_table': 'support',
            },
        ),
    ]