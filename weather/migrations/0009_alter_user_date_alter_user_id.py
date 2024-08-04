# Generated by Django 5.0 on 2024-08-04 12:52

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0008_user_date_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 4, 12, 52, 17, 641591, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('70e8175d-d747-4a43-ac64-0c5b81a7b0bb'), editable=False, primary_key=True, serialize=False),
        ),
    ]
