# Generated by Django 3.2.10 on 2023-05-07 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group_user',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_group_user', to=settings.AUTH_USER_MODEL),
        ),
    ]