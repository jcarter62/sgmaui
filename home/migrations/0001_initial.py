# Generated by Django 4.1.7 on 2023-02-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SessionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.IntegerField(blank=True, default=0, null=True)),
                ('session_id', models.CharField(blank=True, max_length=50, null=True)),
                ('key_name', models.CharField(blank=True, max_length=50, null=True)),
                ('key_text', models.CharField(blank=True, max_length=2048, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['session_id', 'key_name'],
            },
        ),
        migrations.CreateModel(
            name='SystemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting_name', models.CharField(blank=True, max_length=50, null=True)),
                ('setting_text', models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                'ordering': ['setting_name'],
            },
        ),
    ]
