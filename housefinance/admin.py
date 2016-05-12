#encoding:utf-8
# Register your models here.
from django.contrib import admin
from .models import User, Account, AccountingDocumentHeader, AccountingDocumentItem
from decimal import Decimal
from .validations import AccountingDocumentValidation
from django.contrib import messages


# Register your models here.


class AccountingDocumentItemInline(admin.TabularInline):
    model = AccountingDocumentItem
    extra = 0


class AccountingDocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Header Information', {'fields': ['creation_date', 'creator']}),
        ('Comment', {'fields': ['comment']})
    ]
    inlines = [AccountingDocumentItemInline]
    list_display = ('creation_date', 'creator', 'get_total_amount', 'comment')
    list_filter = ['creation_date']
    search_fields = ['comment']

    def save_formset(self, request, form, formset, change):
        acc_doc_header = form.save(commit=False)
        formset.save(commit=False)
        acc_doc_valdt = AccountingDocumentValidation()
        if not acc_doc_valdt.is_document_consistent(request=request,
                                                    changed_objects=formset.changed_objects,
                                                    deleted_objects=formset.deleted_objects,
                                                    new_objects=formset.new_objects,
                                                    acc_doc_header=acc_doc_header):
            if len(acc_doc_header.accountingdocumentitem_set.all()) == 0:
                if request.POST.get('_continue') == None:
                    AccountingDocumentHeader.objects.get(pk=acc_doc_header.id).delete()
            messages.error(request, '记账凭证有错误,不能被保存')
        else:
            # return formset.save()
            return super(AccountingDocumentAdmin, self).save_formset(request, form, formset, change)

    def save_form(self, request, form, change):
        return form.save(commit=False)

admin.site.register(AccountingDocumentHeader, AccountingDocumentAdmin)
admin.site.register(User)
admin.site.register(Account)
