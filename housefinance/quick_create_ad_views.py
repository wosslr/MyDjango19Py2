from django import forms
from .views import AccountingDocumentCreateView


class QuickViewSpend(AccountingDocumentCreateView):
    template_name = 'housefinance/accounting_document/acc_doc_quick_create_spend.html'

    def get_context_data(self, **kwargs):
        context = super(QuickViewSpend, self).get_context_data(**kwargs)
        context['form'].fields['comment'].widget = forms.TextInput()
        return context