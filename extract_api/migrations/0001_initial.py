# Generated by Django 4.1.1 on 2022-09-19 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=100)),
                ('company_info', models.CharField(max_length=500)),
                ('bill_info', models.CharField(max_length=500)),
                ('order', models.CharField(max_length=500)),
                ('total', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
