# Generated by Django 4.2 on 2025-01-18 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0002_profile_old_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_addresses', to='shop.address')),
            ],
            options={
                'verbose_name_plural': 'Shipping Address',
            },
        ),
    ]
