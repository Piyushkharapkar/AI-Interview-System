# Generated by Django 5.1.6 on 2025-03-01 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interviewquestion',
            old_name='difficulty',
            new_name='experience',
        ),
        migrations.AddField(
            model_name='interviewquestion',
            name='expected_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interviewquestion',
            name='skills',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='interviewquestion',
            name='domain',
            field=models.CharField(max_length=255),
        ),
    ]
