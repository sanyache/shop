# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-27 16:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('customer_name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('customer_email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('customer_phone', models.CharField(blank=True, default=None, max_length=48, null=True)),
                ('customer_address', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('comments', models.TextField(blank=True, default=None, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=24, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f',
                'verbose_name_plural': '\u0421\u0442\u0430\u0442\u0443\u0441\u0438 \u0437\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Status'),
        ),
    ]
