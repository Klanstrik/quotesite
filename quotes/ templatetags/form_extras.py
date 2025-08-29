from django import template
register = template.Library()

@register.filter
def add_class(field, css):
    # позволяет писать: {{ field|add_class:"w-full ..." }}
    return field.as_widget(attrs={**field.field.widget.attrs, "class": css})
