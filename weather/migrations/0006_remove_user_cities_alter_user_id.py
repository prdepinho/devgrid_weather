# Generated by Django 5.0 on 2024-08-03 22:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_alter_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cities',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('a38b0bd4-a7ff-4719-b3fc-7365a1e9fed8'), editable=False, primary_key=True, serialize=False),
        ),
    ]
