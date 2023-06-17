# Generated by Django 4.2.2 on 2023-06-17 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('is_complete', models.BooleanField(default=False)),
                ('completed_date', models.DateTimeField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CreatedTasks', to=settings.AUTH_USER_MODEL)),
                ('teams', models.ManyToManyField(related_name='TeamTasks', to='User.team')),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_complete', models.BooleanField(default=False)),
                ('completed_date', models.DateTimeField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SubTasks', to='Task.task')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TeamSubTasks', to='User.team')),
            ],
        ),
    ]
