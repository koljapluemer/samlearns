# Generated by Django 5.2 on 2025-05-20 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triangles', '0002_clozetemplategapprogress_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
            options={
                'unique_together': {('content',)},
            },
        ),
    ]
