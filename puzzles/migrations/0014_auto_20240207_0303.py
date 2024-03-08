# Generated by Django 3.2.17 on 2024-02-07 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("puzzles", "0013_auto_20240202_0125"),
    ]

    operations = [
        migrations.RenameField(
            model_name="team",
            old_name="brown_members",
            new_name="brown_team",
        ),
        migrations.RenameField(
            model_name="team",
            old_name="location",
            new_name="where_to_find",
        ),
        migrations.RemoveField(
            model_name="team",
            name="brown_affiliation_desc",
        ),
        migrations.RemoveField(
            model_name="team",
            name="in_person_sat",
        ),
        migrations.RemoveField(
            model_name="team",
            name="in_person_sun",
        ),
        migrations.RemoveField(
            model_name="team",
            name="merge_in",
        ),
        migrations.RemoveField(
            model_name="team",
            name="merge_in_preferences",
        ),
        migrations.RemoveField(
            model_name="team",
            name="merge_out",
        ),
        migrations.RemoveField(
            model_name="team",
            name="merge_out_preferences",
        ),
        migrations.AddField(
            model_name="team",
            name="num_brown_members",
            field=models.IntegerField(
                default=0,
                help_text="(Undergraduates, Graduates, Faculty, or Alumni)",
                verbose_name="Number of Brown community members on the team",
            ),
        ),
    ]
