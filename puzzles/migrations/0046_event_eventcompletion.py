# Generated by Django 3.2.17 on 2024-04-11 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0045_auto_20240408_0513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp')),
                ('message', models.TextField(verbose_name='Message')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='EventCompletion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_datetime', models.DateTimeField(auto_now=True, verbose_name='Completion datetime')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puzzles.event', verbose_name='event')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puzzles.team', verbose_name='team')),
            ],
            options={
                'verbose_name': 'event completion',
                'verbose_name_plural': 'event completions',
            },
        ),
    ]
