# Generated by Django 5.2 on 2025-05-04 01:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_managers_rename_nombre_beneficiario_alias_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiario',
            name='beneficiario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
