# Generated by Django 4.0.1 on 2022-02-03 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_manager_alter_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager_user', to=settings.AUTH_USER_MODEL, verbose_name='Gerente'),
        ),
    ]
