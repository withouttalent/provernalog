# Generated by Django 2.1.1 on 2018-09-15 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provernalog', '0008_auto_20180914_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuefactor',
            name='evaluative_factor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='provernalog.EvaluativeFactor'),
        ),
        migrations.AlterField(
            model_name='valuefactor',
            name='parcel',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='provernalog.Parcel'),
        ),
        migrations.AlterField(
            model_name='valuefactor',
            name='qualitative_value',
            field=models.CharField(blank=True, max_length=240, verbose_name='Значение качественного фактора'),
        ),
    ]