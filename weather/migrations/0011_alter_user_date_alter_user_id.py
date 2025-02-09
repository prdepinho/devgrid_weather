# Generated by Django 5.0 on 2024-08-04 13:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0010_alter_user_date_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b8d3dc32-5972-45dd-ac8e-4d83e2d7d9bf'), editable=False, primary_key=True, serialize=False),
        ),
    ]
