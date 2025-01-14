# Generated by Django 5.0.6 on 2024-09-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hirexcel_webapp', '0002_cognitive_assessment_results_cognitive_score_percentage_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cognitive_vi_question_dataset',
            old_name='OPTION1',
            new_name='A',
        ),
        migrations.RenameField(
            model_name='cognitive_vi_question_dataset',
            old_name='OPTION2',
            new_name='B',
        ),
        migrations.RenameField(
            model_name='cognitive_vi_question_dataset',
            old_name='OPTION3',
            new_name='C',
        ),
        migrations.RenameField(
            model_name='cognitive_vi_question_dataset',
            old_name='OPTION4',
            new_name='D',
        ),
        migrations.RenameField(
            model_name='cognitive_vi_question_dataset',
            old_name='OPTION5',
            new_name='E',
        ),
        migrations.RenameField(
            model_name='cognitive_vi_question_dataset',
            old_name='OPTION6',
            new_name='F',
        ),
        migrations.RenameField(
            model_name='cognitive_vi_question_dataset',
            old_name='OPTION7',
            new_name='G',
        ),
        migrations.RenameField(
            model_name='cognitive_vi_question_dataset',
            old_name='OPTION8',
            new_name='H',
        ),
        migrations.AlterField(
            model_name='evaluation_summary',
            name='EVALUATION_SUMMARY',
            field=models.FileField(blank=True, null=True, upload_to='hirexcel_webapp/JobSeekerEvaluationSummary/'),
        ),
    ]
