from django import template

register = template.Library()

UK_MONTHS = [
    '', 'січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
    'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'
]

RU_MONTHS = [
    '', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
]

UK_WEEKDAYS = [
    'понеділок', 'вівторок', 'середа', 'четвер', 'пʼятниця', 'субота', 'неділя'
]

RU_WEEKDAYS = [
    'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'
]
WEEKDAYS_SHORT = [
    'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'
]

@register.filter
def format_date_localized(date, lang='uk'):
    if not date:
        return ''
    day = date.day
    month = date.month
    if lang == 'ru':
        return f"{day} {RU_MONTHS[month]}"
    return f"{day} {UK_MONTHS[month]}"


@register.filter
def format_date_localized_schedule(date, lang='uk'):
    if not date:
        return ''
    day = date.day
    month = date.month
    weekday = date.weekday()

    if lang == 'ru':
        return f"{day} {RU_MONTHS[month]}, {RU_WEEKDAYS[weekday]}"
    return f"{day} {UK_MONTHS[month]}, {UK_WEEKDAYS[weekday]}"



@register.filter
def format_date_localized_reverse_ticket(date, lang='uk'):
    if not date:
        return ''
    day = date.day
    month = date.month
    formatted_time = date.time().strftime('%H:%M')

    if lang == 'ru':
        return f"{day} {RU_MONTHS[month]}, {formatted_time}"
    return f"{day} {UK_MONTHS[month]}, {formatted_time}"


@register.filter
def format_date_month(date, lang='uk'):
    if not date:
        return ''

    month = date.month
    if lang == 'ru':
        return f"{RU_MONTHS[month]}"
    return f"{UK_MONTHS[month]}"

@register.filter
def format_date_weekdays_short(date):
    if not date:
        return ''
    day = date.day
    weekday = date.weekday()

    return f"{day} {WEEKDAYS_SHORT[weekday]}"