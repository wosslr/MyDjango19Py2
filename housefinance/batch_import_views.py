#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .constants import LOGIN_URL

from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from django.template import RequestContext
from django.views.generic import View

from datetime import datetime

from .models import AccountingDocumentHeader, AccountingDocumentItem, Account, User
from .forms import AccountingDocumentFormSet


class ZFBImportView(View):
    @method_decorator(login_required(login_url=LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        return super(ZFBImportView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        context.update(csrf(request))
        return render_to_response(template_name='housefinance/batch_import/batch_import_zfb_step1.html', context=context)

    def post(self, request, *args, **kwargs):
        if request.FILES:
            txtfile = request.FILES['txt_file']
            start_flag = False
            accountingDocuments = []
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

                        accountingDocuments.append({
                            'header': acc_doc,
                            'items': [acc_item1, acc_item2]
                        })
                for value in values:
                    value = value.strip()
                    if value == '交易号':
                        start_flag = True
                        break

            context = {}
            context.update(csrf(request))
            context['acc_docs'] = accountingDocuments
            return render_to_response(template_name='housefinance/batch_import/batch_import_zfb_step2.html', context=context)
        else:
            print(dir(request.POST))
            print(request.POST.get('test'))
            return self.get(request, *args, **kwargs)


@login_required(login_url=LOGIN_URL)
def batch_import_zfb_upload(request):
    if request.method == 'POST' and request.FILES:
        txtfile = request.FILES['txt_file']
        start_flag = False
        accountingDocuments = []
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

                    accountingDocuments.append({
                        'header': acc_doc,
                        'items': [acc_item1, acc_item2]
                    })
            for value in values:
                value = value.strip()
                if value == '交易号':
                    start_flag = True
                    break

        context = {}
        context.update(csrf(request))
        context['acc_docs'] = accountingDocuments
        return render_to_response(template_name='housefinance/batch_import/batch_import_zfb_step2.html', context=context)
    elif request.method == 'GET':
        context = {}
        context.update(csrf(request))
        return render_to_response(template_name='housefinance/batch_import/batch_import_zfb_step1.html', context=context)


@login_required(login_url=LOGIN_URL)
def batch_import_acc_doc_import(request):
    print(dir(request.POST))