# Generated by Django 3.2.17 on 2024-04-02 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0039_minorcaseincomingevent_num_votes_allowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='unlock_hours',
            field=models.IntegerField(default=-1, help_text='If nonnegative, round unlocks N hours after the hunt starts.', verbose_name='Unlock hours'),
        ),
    ]
