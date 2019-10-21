# Generated by Django 2.1.2 on 2018-10-12 09:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provernalog', '0017_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('region',), 'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
        migrations.AddField(
            model_name='parcel',
            name='cost_pre_intermediate',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=21), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='parcel',
            name='specific_cost_pre_intermediate',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=21), blank=True, null=True, size=None),
        ),
    ]