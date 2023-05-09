# Generated by Django 3.2.10 on 2023-05-01 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='group_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, default='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_group_user', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='group_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
