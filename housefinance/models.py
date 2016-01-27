#encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as SysUser

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_role = models.CharField(max_length=10, blank=True)
    sys_user = models.OneToOneField(SysUser, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Account(models.Model):
    ACCOUNT_TYPE_OPTIONS = (
        ('ZC', '资产'),
        ('CB', '成本'),
        ('FY', '费用'),
        ('FZ', '负债'),
        ('SR', '收入'),
    )
    account_name = models.CharField(max_length=50)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_OPTIONS)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.account_name


class AccountingDocumentHeader(models.Model):
    creation_date = models.DateTimeField("记账日期")
    creator = models.ForeignKey(User, verbose_name='创建人')
    comment = models.TextField(blank=True, verbose_name='备注')

    def __str__(self):
        return self.creation_date.date().__str__() + ' ' + self.id.__str__() + ' ' + self.comment



class AccountingDocumentItem(models.Model):
    DEBIT_CREDIT_INDICATOR_OPTIONS = (
        ('J', '借方'),
        ('D', '贷方'),
    )
    dc_indicator = models.CharField(max_length=1, choices=DEBIT_CREDIT_INDICATOR_OPTIONS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    document_header = models.ForeignKey(AccountingDocumentHeader)
    account = models.ForeignKey(Account)
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.document_header.__str__() + ' ' + self.id.__str__()


