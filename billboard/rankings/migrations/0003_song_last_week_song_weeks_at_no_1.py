# Generated by Django 5.0.6 on 2024-06-04 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0002_alter_user_email_alter_favorite_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='last_week',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='weeks_at_no_1',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
