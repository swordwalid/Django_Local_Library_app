from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('LocalLibrary', '0009_remove_genre_genre_name_case_insensitive_unique_and_more'),  # Replace with your last migration
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='genre',
            name='genre_name_case_insensitive_unique',
        ),
        migrations.RemoveConstraint(
            model_name='language',
            name='language_name_case_insensitive_unique',  # Assuming this is the constraint name
        ),
    ]