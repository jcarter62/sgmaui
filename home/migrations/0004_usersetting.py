# Generated by Django 4.1.7 on 2023-03-17 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_sessiondata_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.IntegerField(blank=True, default=0, null=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('key_name', models.CharField(blank=True, max_length=50, null=True)),
                ('key_text', models.CharField(blank=True, max_length=2048, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['username', 'key_name', 'key_text'],
            },
        ),
    ]
