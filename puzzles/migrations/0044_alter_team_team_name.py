# Generated by Django 3.2.17 on 2024-04-07 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0043_alter_minorcasevoteevent_selected_cases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(help_text='Public team name for scoreboards and communications', max_length=423, unique=True, verbose_name='Team name'),
        ),
    ]
