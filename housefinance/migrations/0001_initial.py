# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-23 04:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=50)),
                ('account_type', models.CharField(choices=[('ZC', '\u8d44\u4ea7'), ('CB', '\u6210\u672c'), ('FY', '\u8d39\u7528'), ('FZ', '\u8d1f\u503a'), ('SR', '\u6536\u5165')], max_length=10)),
                ('account_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='AccountingDocumentHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(verbose_name='\u8bb0\u8d26\u65e5\u671f')),
                ('comment', models.TextField(blank=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='AccountingDocumentItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dc_indicator', models.CharField(choices=[('J', '\u501f\u65b9'), ('D', '\u8d37\u65b9')], max_length=1)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housefinance.Account')),
                ('document_header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housefinance.AccountingDocumentHeader')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user_role', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='accountingdocumentheader',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housefinance.User', verbose_name='\u521b\u5efa\u4eba'),
        ),
    ]