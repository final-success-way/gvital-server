# Generated by Django 2.2.16 on 2022-03-04 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_requestparameters_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseParameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('parameter', models.CharField(blank=True, max_length=50)),
                ('parameter_type', models.CharField(blank=True, max_length=50)),
                ('value', models.CharField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
