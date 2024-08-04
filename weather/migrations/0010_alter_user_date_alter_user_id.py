# Generated by Django 5.0 on 2024-08-04 12:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0009_alter_user_date_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ea0f3964-41b4-440c-8815-21d1f778583d'), editable=False, primary_key=True, serialize=False),
        ),
    ]
