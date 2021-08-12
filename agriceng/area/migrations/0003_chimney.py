# Generated by Django 3.1.13 on 2021-08-04 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0002_auto_20210802_0755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chimney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('velocity', models.IntegerField()),
                ('width', models.DecimalField(decimal_places=3, max_digits=4)),
                ('depth', models.DecimalField(decimal_places=1, max_digits=2)),
            ],
        ),
    ]