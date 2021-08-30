# Generated by Django 3.1.13 on 2021-08-30 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solardryers', '0004_auto_20210731_2107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['dryer', 'created', 'modified', 'note']},
        ),
        migrations.AddConstraint(
            model_name='dryer',
            constraint=models.UniqueConstraint(fields=('size', 'version'), name='unique_dryer'),
        ),
    ]