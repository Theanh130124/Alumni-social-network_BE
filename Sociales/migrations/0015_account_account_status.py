# Generated by Django 5.1.3 on 2024-12-25 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sociales', '0014_remove_user_avatar_remove_user_cover_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_status',
            field=models.BooleanField(default=False),
        ),
    ]