# Generated by Django 5.1.1 on 2024-09-23 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0017_owed_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='profit_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.TextField(max_length=20000)),
                ('profit', models.IntegerField()),
                ('extra', models.TextField(max_length=20000)),
                ('extra_profit', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
