from datetime import date, timedelta


class MyDateUtility:
    @staticmethod
    def get_first_day_of_month(p_date):
        return p_date.replace(day=1)

    @staticmethod
    def get_last_day_of_month(p_date):
        if p_date.month == 12:
            return p_date.replace(day=31)
        return p_date.replace(month=p_date.month + 1, day=1) - timedelta(days=1)