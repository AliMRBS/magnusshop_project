# Generated by Django 4.2 on 2025-01-21 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_alter_orderitem_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='last_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
