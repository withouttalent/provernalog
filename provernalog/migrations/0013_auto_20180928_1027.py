# Generated by Django 2.1.1 on 2018-09-28 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provernalog', '0012_auto_20180928_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subgroupappraise',
            name='group',
        ),
        migrations.AddField(
            model_name='parcel',
            name='subgroup_appraise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='provernalog.SubgroupAppraise'),
        ),
    ]
