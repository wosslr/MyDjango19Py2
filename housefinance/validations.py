#encoding:utf-8
from __future__ import unicode_literals
from .models import AccountingDocumentHeader, AccountingDocumentItem
from decimal import Decimal
from django.contrib import messages


class AccountingDocumentValidation:

    def is_document_consistent(self, request, **kwargs):
        amount_j = Decimal(0)
        amount_d = Decimal(0)

        changed_objects = kwargs['changed_objects']
        deleted_objects = kwargs['deleted_objects']
        new_objects = kwargs['new_objects']
        acc_doc_header = kwargs['acc_doc_header']

        for acc_item_chg in changed_objects:
            if acc_item_chg[0].dc_indicator == 'J':
                amount_j += acc_item_chg[0].amount
            else:
                amount_d += acc_item_chg[0].amount

        for acc_item_new in new_objects:
            if acc_item_new.dc_indicator == 'J':
                amount_j += acc_item_new.amount
            else:
                amount_d += acc_item_new.amount

        for acc_item_del in deleted_objects:
            if acc_item_del.dc_indicator == 'J':
                amount_j -= acc_item_del.amount
            else:
                amount_d -= acc_item_del.amount

        if amount_j != amount_d:
            messages.error(request, '记账凭证金额不平')
            return False
        else:
            if amount_d == 0:
                if len(acc_doc_header.accountingdocumentitem_set.all()) == 0:
                    messages.error(request, '记账凭证不能没有发生金额')
                else:
                    return True
            else:
                return True

