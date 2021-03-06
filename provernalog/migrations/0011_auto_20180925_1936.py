# Generated by Django 2.1.1 on 2018-09-25 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provernalog', '0010_auto_20180915_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='approved_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=21, null=True, verbose_name='Утвержденная стоимость'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='approved_specififc_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=21, null=True, verbose_name='УПКС утвержденной стоимости'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='cost_intermediate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=21, null=True, verbose_name='Ожидаемая стоимость'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='current_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=21, null=True, verbose_name='Текущая стоимость'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='current_specific_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=21, null=True, verbose_name='УПКС текущей стоимости'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='specific_cost_intermediate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=21, null=True, verbose_name='УПКС ожидаемой стоимости'),
        ),
    ]
