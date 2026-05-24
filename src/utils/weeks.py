import calendar
import datetime

def calculate_weeks(additional_month = 0):
    now = datetime.datetime.now()
    target_month_index = now.month + additional_month
    current_year = now.year + (target_month_index - 1) // 12
    current_month = ((target_month_index - 1) % 12) + 1
    
    if current_month == 12:
        next_year = current_year + 1
        next_month = 1
    else:
        next_year = current_year
        next_month = current_month + 1

    first_day_next_month = datetime.date(next_year, next_month, 1)
    first_monday = first_day_next_month + datetime.timedelta(days=(0 - first_day_next_month.weekday()) % 7)
    days_in_the_month = calendar.monthrange(next_year, next_month)[1]

    weeks = []

    start_of_week = first_monday
    for day in range(first_monday.day, days_in_the_month + 1):
        date = datetime.date(next_year, next_month, day)
        if date.weekday() == 0:
            start_of_week = date
        if date.weekday() == 6 or day == days_in_the_month:
            end_of_week = date
            weeks.append((start_of_week, end_of_week))
            start_of_week = None

    last_week = weeks[-1]
    last_monday_of_the_month = last_week[0]
    weeks[-1] = (last_monday_of_the_month, last_monday_of_the_month + datetime.timedelta(days=6))
    
    return weeks

def format_week(week):
    formatted_week = ""
    months_in_spansh = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    current_month = months_in_spansh[week[0].month - 1]
    if week[0].month == week[1].month:
        formatted_week = f"Semana del {week[0].day} - {week[1].day} de {current_month.capitalize()}"
    else:
        if (week[0].month >= 12):
            next_month = months_in_spansh[0]
        else:
            next_month = months_in_spansh[week[0].month]
        formatted_week = f"Semana del {week[0].day} de {current_month.capitalize()} al {week[1].day} de {next_month.capitalize()}"

    return formatted_week
