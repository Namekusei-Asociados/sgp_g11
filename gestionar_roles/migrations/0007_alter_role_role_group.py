# Generated by Django 4.1 on 2022-09-08 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('gestionar_roles', '0006_alter_role_role_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
    ]
