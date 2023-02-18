# Generated by Django 2.2.16 on 2022-03-03 13:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendors', '0003_requestparameters_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('question', models.CharField(blank=True, max_length=200)),
                ('answer', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(choices=[('INSTAGRAM', 'INSTAGRAM'), ('YOUTUBE', 'YOUTUBE'), ('TWITTER', 'TWITTER'), ('TWITCH', 'TWITCH'), ('SOUNDCLOUD', 'SOUNDCLOUD'), ('SPOTIFY', 'SPOTIFY'), ('FACEBOOK', 'FACEBOOK'), ('LINKEDIN', 'LINKEDIN'), ('TIKTOK', 'TIKTOK')], default='INSTAGRAM', max_length=100)),
                ('order', models.IntegerField(default=1, max_length=3)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=350, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('author', models.CharField(blank=True, max_length=200)),
                ('review', models.TextField()),
                ('rating', models.CharField(blank=True, max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Varient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('original_price', models.CharField(default='0', max_length=10)),
                ('discounted_price', models.CharField(default='0', max_length=10)),
                ('percent_discount', models.CharField(default='0', max_length=10)),
                ('currency', models.CharField(default='USD', max_length=10)),
                ('quantity', models.IntegerField(default=10, max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=350, null=True)),
                ('seo_title', models.TextField(blank=True, null=True)),
                ('seo_description', models.TextField(blank=True, null=True)),
                ('seo_keywords', models.TextField(blank=True, null=True)),
                ('meta_message', models.TextField(blank=True, max_length=250, null=True)),
                ('button_message', models.CharField(blank=True, max_length=200, null=True)),
                ('real_users', models.BooleanField(default=True)),
                ('needs_meta', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('api', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendors.VendorApi')),
                ('faq', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.FAQ')),
                ('platform', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Platform')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Review')),
                ('varients', models.ManyToManyField(to='services.Varient')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]