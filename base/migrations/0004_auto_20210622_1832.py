# Generated by Django 3.2.3 on 2021-06-22 15:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ShippingPrice',
            new_name='shippingPrice',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='TaxPrice',
            new_name='taxPrice',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updatedAt',
        ),
        migrations.AddField(
            model_name='review',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='_id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='_id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='/placeholder.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='review',
            name='_id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='_id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]