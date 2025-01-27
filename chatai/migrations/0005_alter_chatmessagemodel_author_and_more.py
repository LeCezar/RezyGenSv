# Generated by Django 5.1 on 2024-09-02 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatai', '0004_auto_20240829_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessagemodel',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='chatai.authortype'),
        ),
        migrations.AlterField(
            model_name='chatmessagemodel',
            name='content',
            field=models.TextField(editable=False),
        ),
    ]
