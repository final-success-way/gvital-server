# Generated by Django 2.2.16 on 2022-03-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_faq_is_general'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='service',
            name='faqs',
            field=models.ManyToManyField(blank=True, default=None, to='services.FAQ'),
        ),
        migrations.AlterField(
            model_name='varient',
            name='quantity',
            field=models.IntegerField(default=10, null=True),
        ),
    ]
