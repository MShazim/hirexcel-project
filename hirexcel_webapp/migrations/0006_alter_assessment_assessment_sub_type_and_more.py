# Generated by Django 5.0.6 on 2024-06-11 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hirexcel_webapp', '0005_alter_job_posting_jpc_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='ASSESSMENT_SUB_TYPE',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='REQUIRED_COMPLETION_TIME',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job_seeker_assessment',
            name='ASSESSMENT_ONGOING_STATUS',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job_seeker_assessment',
            name='COMPLETION_TIME',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job_seeker_assessment',
            name='NAME',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]