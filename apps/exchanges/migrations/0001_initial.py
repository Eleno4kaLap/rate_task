# Generated by Django 3.2.11 on 2022-04-26 10:09

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('rate', models.DecimalField(decimal_places=8, max_digits=16)),
                ('base_asset', models.CharField(max_length=6)),
                ('quote_asset', models.CharField(max_length=6)),
                ('last_updated', models.DateTimeField()),
            ],
            options={
                'ordering': ('-last_updated',),
            },
        ),
    ]
