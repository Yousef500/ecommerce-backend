# Generated by Django 3.2.3 on 2021-06-25 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20210622_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='/sample.png', null=True, upload_to=''),
        ),
    ]