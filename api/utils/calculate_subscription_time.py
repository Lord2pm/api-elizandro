from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_subscrption_time(qtd_meses) -> datetime:
    return datetime.now() + relativedelta(months=qtd_meses)


def verify_subscrption_time(data_termino: datetime) -> bool:
    if (
        data_termino.day == datetime.now().day
        and data_termino.month == datetime.now().month
    ):
        return True

    return False
