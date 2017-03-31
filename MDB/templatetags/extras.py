from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter
def get_item(dictionary, key):
    print "Dictonary: {0}".format(dictionary)
    print "Key: {0}".format(key)
    return dictionary.get(key)
