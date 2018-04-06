import re
from django import template

register = template.Library()

@register.filter
def hyphenate(value):
    """
      Normalizes string, converts to lowercase, removes non-alpha
      characters, and converts spaces to hyphens.
    """
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)
