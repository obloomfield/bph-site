# Generated by Django 3.2.17 on 2024-03-30 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0037_minorcaseincomingevent_total_user_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='minorcaseincomingevent',
            name='incoming_cases',
            field=models.ManyToManyField(blank=True, related_name='cases', to='puzzles.Round', verbose_name='Cases'),
        ),
    ]
