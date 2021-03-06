# Generated by Django 3.1 on 2020-09-18 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_auto_20200913_0024'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_exam_marks', models.FloatField(default=0)),
                ('subject_assignment_marks', models.FloatField(default=0)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.subjects')),
            ],
        ),
    ]
