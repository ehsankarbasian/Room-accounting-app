# Generated by Django 3.2.8 on 2022-04-06 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountingApp', '0008_auto_20211019_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='reset_pass_code',
            field=models.IntegerField(default=217837),
        ),
        migrations.AlterField(
            model_name='token',
            name='reset_pass_token',
            field=models.CharField(default='f97f45677d43d9121b90ba5b1e1281a9361d6ef3634c7e8a5d865da8ff6e455a9b43d4a5c66b36b2a98b0ec6ecaf56f5a0cd505544d4f07c5a1d2a165ca6d0af', max_length=64),
        ),
    ]
