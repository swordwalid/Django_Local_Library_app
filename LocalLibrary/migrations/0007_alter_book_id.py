# Generated by Django 5.1.4 on 2025-01-07 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LocalLibrary', '0006_alter_book_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
