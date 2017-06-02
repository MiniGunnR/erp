from datetime import datetime
import calendar


def now(request):
    now = datetime.now()
    context = {
        "current_year": now.year,
        "current_month": calendar.month_name[now.month],
        "current_month_number": now.month,
    }
    return context

