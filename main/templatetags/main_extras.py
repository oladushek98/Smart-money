from django import template

register = template.Library()


@register.filter(name='is_current_page')
def is_checkbox(field):
    var = {
        'user': 1,
        'edit': 3,
        'parameters': 2,
        'transaction': 4,
        'bank': 5,
    }

    return var[field.split('/')[-1] if field.split('/')[-1]
    else field.split('/')[-2]]


@register.filter(name='get_date_from')
def get_data_from(field):
    if 'from' in field.GET:
        return field.GET['from']
    else:
        return False


@register.filter(name='get_date_to')
def get_data_to(field):
    if 'to' in field.GET:
        return field.GET['to']
    else:
        return False


@register.filter(name='get_date_start')
def get_data_start(field):
    if 'start' in field.GET:
        return field.GET['start']
    else:
        return False


@register.filter(name='get_date_tail')
def get_data_tail(field, count):
    start = get_data_start(field)
    if start and count:
        return str(int(start) + int(count))
    else:
        return 0


@register.filter(name='get_date_end')
def get_data_end(field):
    if 'end' in field.GET:
        return field.GET['end']
    else:
        return False


@register.filter(name='get_date_count')
def get_date_count(field):
    start = get_data_start(field)
    end = get_data_end(field)
    if start and end:
        return str(int(end) - int(start))
    else:
        return 0
