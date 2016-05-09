from django.conf.urls import url
from . import views
from . import quick_create_ad_views, batch_import_views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^accounting_document/$', views.AccountingDocumentIndexView.as_view(), name='acc_doc_index'),
    url(r'^accounting_document/(?P<pk>[0-9]+)/$', views.AccountingDocumentDetailView.as_view(), name='acc_doc_detail'),
    url(r'^accounting_document/add/$', views.AccountingDocumentCreateView.as_view(success_url='/ffm/accounting_document'), name='acc_doc_add'),
    url(r'^accounting_document/quick_add_spend/$', quick_create_ad_views.QuickViewSpend.as_view(success_url='/ffm/accounting_document'), name='acc_doc_quick_add_spend'),
    url(r'^chart_spend/$', views.chart_spend, name='chart_spend'),
    url(r'^fibonacci/(?P<m>[0-9]+)$', views.fibonacci, name='fibonacci'),
    url(r'^chart_spend_monthly/$', views.chart_spend_monthly, name='chart_spend_monthly'),
    url(r'^batch_import_acc_doc_upload/$', batch_import_views.ZFBImportView.as_view(), name='batch_import_zfb_upload'),
    url(r'^batch_import_acc_doc_import/$', batch_import_views.batch_import_acc_doc_import, name='batch_import_acc_doc_import'),
]