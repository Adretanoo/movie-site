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

@register.filter
def format_date_localized(date, lang='uk'):
    if not date:
        return ''
    day = date.day
    month = date.month
    if lang == 'ru':
        return f"{day} {RU_MONTHS[month]}"
    return f"{day} {UK_MONTHS[month]}"
