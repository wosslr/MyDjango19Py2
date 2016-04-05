#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .constants import LOGIN_URL

from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf

from datetime import datetime

from .models import AccountingDocumentHeader, AccountingDocumentItem, Account, User
from .forms import AccountingDocumentFormSet


@login_required(login_url=LOGIN_URL)
def batch_import_zfb(request):
    if request.method == 'POST' and request.FILES:
        txtfile = request.FILES['txt_file']
        start_flag = False
        accountingDocuments = []
        accountingDocumentItems = []
        account_fy = Account.objects.filter(account_type='FY')[:1].get()
        account_zc = Account.objects.filter(account_type='ZC')[:1].get()
        curr_user = User.objects.filter(sys_user=request.user)[:1].get()
        for line in txtfile:
            values = line.split(',')
            if start_flag and len(values) > 14:
                for i in range(0, len(values)):
                    values[i] = values[i].strip()
                if values[10] == '支出' and values[11] == '交易成功' and values[5] != '支付宝网站':
                    acc_doc = AccountingDocumentHeader()
                    acc_doc.creation_date = datetime.strptime(values[3], '%Y-%m-%d %H:%M:%S')
                    acc_doc.creator = curr_user
                    acc_doc.comment = values[8]
                    acc_item1 = AccountingDocumentItem()
                    acc_item1.dc_indicator = 'J'
                    acc_item1.amount = values[9]
                    acc_item1.document_header = acc_doc
                    acc_item1.account = account_fy

                    acc_item2 = AccountingDocumentItem()
                    acc_item2.dc_indicator = 'D'
                    acc_item2.amount = values[9]
                    acc_item2.document_header = acc_doc
                    acc_item2.account = account_zc

                    accountingDocuments.append(acc_doc)
                    accountingDocumentItems.append(acc_item1)
                    accountingDocumentItems.append(acc_item2)

            for value in values:
                value = value.strip()
                if value == '交易号':
                    start_flag = True
                    break

        acc_doc_formset = AccountingDocumentFormSet(instance=accountingDocuments)
        print(acc_doc_formset)
        context = {}
        context['acc_docs'] = accountingDocuments
        context['acc_doc_items']  =accountingDocumentItems
        return render_to_response(template_name='housefinance/batch_import/batch_import_zfb_step2.html', context=context)
    elif request.method == 'GET':
        context = {}
        context.update(csrf(request))
        return render_to_response(template_name='housefinance/batch_import/batch_import_zfb_step1.html', context=context)