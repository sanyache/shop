# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-21 08:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0002_auto_20180516_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, default=None, max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, default=None, max_length=200, null=True, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='myshop.Category', verbose_name='\u0411\u0440\u0435\u043d\u0434')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u0411\u0440\u0435\u043d\u0434',
                'verbose_name_plural': '\u0411\u0440\u0435\u043d\u0434\u0438',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='myshop.Category', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u044f'),
        ),
        migrations.AddField(
            model_name='product',
            name='brend',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='myshop.Brand', verbose_name='\u0411\u0440\u0435\u043d\u0434'),
        ),
    ]
