# Generated by Django 5.1.4 on 2025-01-10 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_letter_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameimage',
            name='description',
            field=models.TextField(blank=True, default='This is and alphabet', max_length=100, null=True),
        ),
    ]
