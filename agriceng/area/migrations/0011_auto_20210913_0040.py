# Generated by Django 3.1.13 on 2021-09-12 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0010_auto_20210902_1007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coefficient',
            options={'ordering': ['created']},
        ),
    ]
