from django.utils import timezone

from .models import AccountingDocumentHeader, AccountingDocumentItem
from .utilities import MyDateUtility


class ChartSpendMonthlyHelper:
    @staticmethod
    def get_periods():
        result = dict()
        acc_header_list = AccountingDocumentHeader.objects.all().values('creation_date').distinct()
        for acc_header in acc_header_list.iterator():
            acc_header_date = acc_header['creation_date']
            key = str(acc_header_date.year) + str(acc_header_date.month)
            result[key] = {'year': acc_header_date.year, 'month': acc_header_date.month}
        return result

    @staticmethod
    def get_spend_data_by_month(p_year, p_month):
        query_date = timezone.now()
        query_date_start = query_date.replace(year=p_year, month=p_month, day=1)
        query_date_end = MyDateUtility.get_last_day_of_month(query_date)
        acc_doc_items = AccountingDocumentItem.objects.filter(
                account__account_type='FY',
                document_header__creation_date__range=[query_date_start,
                                                       query_date_end]
        ).order_by(
                'document_header__creation_date')

        chart_data_set = []

        for i in range(query_date_start.day, query_date_end.day + 1):
            lv_amount = 0
            for acc_doc_item in acc_doc_items:
                if acc_doc_item.document_header.creation_date.day == i:
                    lv_amount += acc_doc_item.amount
            chart_data_set.append({
                'date': {
                    'year': p_year,
                    'month': p_month,
                    'day': i
                },
                'amount': lv_amount
            })
        return chart_data_set
