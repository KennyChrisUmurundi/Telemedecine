# Generated by Django 3.2.9 on 2021-12-08 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_institution_default_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_role', to=settings.AUTH_USER_MODEL),
        ),
    ]