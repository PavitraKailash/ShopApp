# Generated by Django 3.2.7 on 2021-09-22 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdetails',
            name='created_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
