# Generated by Django 5.0.1 on 2024-01-25 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_pack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewCoursePack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('course_pack', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course_pack.coursepack')),
            ],
        ),
    ]
