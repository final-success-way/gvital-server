# Generated by Django 2.2.16 on 2022-03-04 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20220304_1136'),
        ('orders', '0003_auto_20220304_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='varient',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='services.Varient'),
        ),
    ]
