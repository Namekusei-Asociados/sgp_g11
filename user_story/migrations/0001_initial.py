# Generated by Django 4.1 on 2022-09-26 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('type_us', '0002_typeus_project'),
        ('projects', '0004_roleproject_project_alter_project_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=100)),
                ('business_value', models.IntegerField()),
                ('technical_priority', models.IntegerField()),
                ('estimation_time', models.IntegerField()),
                ('current_status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('assigned_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.projectmember')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('us_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='type_us.typeus')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
    ]
