# Generated by Django 5.0.6 on 2024-09-30 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hirexcel_webapp', '0003_rename_option1_cognitive_vi_question_dataset_a_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='A',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='ANSWER',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='B',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='C',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='D',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='E',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='F',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='G',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='cognitive_vi_question_dataset',
            name='H',
            field=models.CharField(max_length=1000),
        ),
    ]
