from django import template

register = template.Library()

@register.filter(name='usernames')
def usernames(value):
    return ", ".join(i.username for i in value)
