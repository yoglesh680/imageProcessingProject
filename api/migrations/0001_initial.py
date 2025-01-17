# Generated by Django 5.0.7 on 2024-07-15 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField()),
                ('product_name', models.CharField(max_length=100)),
                ('input_image_urls', models.TextField()),
                ('output_image_urls', models.TextField(blank=True, null=True)),
                ('request_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
