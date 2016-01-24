#encoding:utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import AccountingDocumentForm, AccountingDocumentItemFormSet
from .models import AccountingDocumentHeader, AccountingDocumentItem
from .validations import AccountingDocumentValidation
from datetime import datetime
from .funs import fib
from .helpers import ChartSpendMonthlyHelper
from .constants import LOGIN_URL


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'housefinance/index.html'
    context_object_name = 'account_doc_list'

    def get_queryset(self):
        return AccountingDocumentHeader.objects.order_by('-creation_date')

    @method_decorator(login_required(login_url=LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class AccountingDocumentIndexView(generic.ListView):
    template_name = 'housefinance/accounting_document/index.html'
    context_object_name = 'account_doc_list'

    def get_queryset(self):
        return AccountingDocumentHeader.objects.order_by('-creation_date')

    @method_decorator(login_required(login_url=LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        return super(AccountingDocumentIndexView, self).dispatch(request, *args, **kwargs)


class AccountingDocumentDetailView(generic.DetailView):
    model = AccountingDocumentHeader
    context_object_name = 'account_doc'
    template_name = 'housefinance/accounting_document/detail.html'

    @method_decorator(login_required(login_url=LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        return super(AccountingDocumentDetailView, self).dispatch(request, *args, **kwargs)


class AccountingDocumentCreateView(generic.CreateView):
    model = AccountingDocumentHeader
    # fields = ['creation_date', 'creator', 'comment']
    form_class = AccountingDocumentForm
    template_name = 'housefinance/accounting_document/acc_doc_create.html'

    def get_context_data(self, **kwargs):
        context = super(AccountingDocumentCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = AccountingDocumentForm(self.request.POST)
            context['formset'] = AccountingDocumentItemFormSet(self.request.POST)
        else:
            context['form'] = AccountingDocumentForm(initial={
                'creation_date': '{0:%Y/%m/%d %H:%M}'.format(datetime.now()),
                'creator': self.request.user
            })
            context['formset'] = AccountingDocumentItemFormSet()
        # context['formset'] = AccountingDocumentItemFormSet(queryset=AccountingDocumentItem.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = AccountingDocumentForm(request.POST)
        # acc_doc_header = form.save(commit=False)
        # formset = AccountingDocumentItemFormSet(request.POST)
        if not form.is_valid():
            return self.render_to_response(context=self.get_context_data(
                    # form=form,
                    # formset=formset
            ))
        acc_doc_header = form.save(commit=False)
        print acc_doc_header.creation_date
        formset = AccountingDocumentItemFormSet(request.POST, instance=acc_doc_header)
        # context = {'form': form,
        #            'formset': formset}
        if formset.is_valid():
            acc_doc_items = formset.save(commit=False)
            if not AccountingDocumentValidation().is_document_consistent(
                    request=request,
                    changed_objects=formset.changed_objects,
                    deleted_objects=formset.deleted_objects,
                    new_objects=formset.new_objects,
                    acc_doc_header=acc_doc_header
            ):
                return self.render_to_response(context=self.get_context_data(
                        # form=form,
                        # formset=formset
                ))
                # return render(request, template_name='housefinance/accounting_document/acc_doc_create.html',
                #               context=context)
            else:
                self.object = acc_doc_header = form.save(commit=True)
                formset.instance = self.object
                acc_doc_items = formset.save(commit=True)
                messages.success(request=request,
                                 message='凭证 ' + acc_doc_header.__str__() + ' 创建成功')
                return HttpResponseRedirect('/ffm/accounting_document')
        else:
            return self.render_to_response(
                    self.get_context_data(
                            # form=form, formset=formset
                    )
            )

    @method_decorator(login_required(login_url=LOGIN_URL))
    def dispatch(self, request, *args, **kwargs):
        return super(AccountingDocumentCreateView, self).dispatch(request, *args, **kwargs)


@login_required(login_url=LOGIN_URL)
def chart_spend(request):
    acc_doc_items = AccountingDocumentItem.objects.filter(account__account_type='FY').order_by(
            'document_header__creation_date')
    for acc_doc_item in acc_doc_items:
        if not acc_doc_item.comment:
            if not acc_doc_item.document_header.comment:
                acc_doc_item.comment = acc_doc_item.account.account_name
            else:
                acc_doc_item.comment = acc_doc_item.document_header.comment

    context = {'acc_doc_items': acc_doc_items}
    return render(request=request, template_name='housefinance/chart_spend.html', context=context)


@login_required(login_url=LOGIN_URL)
def fibonacci(request, m):
    tm = int(m)
    context = {'fibonacci': fib(tm)}
    return render(request=request, template_name='housefinance/fibonacci.html', context=context)


@login_required(login_url=LOGIN_URL)
def chart_spend_monthly(request):
    print(request.GET)
    context = dict()
    context['periods'] = ChartSpendMonthlyHelper.get_periods()
    context['chart_data_set'] = ChartSpendMonthlyHelper.get_spend_data_by_month(2016, 1)
    return render(request=request, template_name='housefinance/charts/monthly_spend_chart.html', context=context)
