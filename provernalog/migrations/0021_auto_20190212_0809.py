# Generated by Django 2.1.2 on 2019-02-12 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provernalog', '0020_auto_20190211_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='address',
            field=models.CharField(blank=True, max_length=960, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='city',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='words/'),
        ),
    ]