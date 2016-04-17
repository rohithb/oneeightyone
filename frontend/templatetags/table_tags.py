from django import template
import re

register = template.Library()


@register.simple_tag
def print_row(row, contents, columns):
    row_html = ''
    column_names = columns
    for col in column_names:
        row_html += '<td>' + str(getattr(row,contents.model_fields[col].get_attname())) + '</td>'
    return row_html

@register.simple_tag
def convert_attribute_name(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    s2 = s2.replace('_', ' ')
    return s2.title()

@register.simple_tag
def print_row_from_tuple(row):
    row_html = ['<td>%s</td>'%data for data in row]
    return ''.join(row_html)
    