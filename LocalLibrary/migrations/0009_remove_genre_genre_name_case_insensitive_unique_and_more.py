# Generated by Django 5.1.4 on 2025-01-15 07:13

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LocalLibrary', '0008_remove_genre_genre_name_case_insensitive_unique_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='genre',
            name='genre_name_case_insensitive_unique',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='name_lower',
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)', max_length=200, unique=True),
        ),
        migrations.AddConstraint(
            model_name='genre',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='genre_name_case_insensitive_unique', violation_error_message='Genre already exists (case insensitive match)'),
        ),
    ]
