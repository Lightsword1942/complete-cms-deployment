from django.utils.importlib import import_module
from django import template

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

register = template.Library()

class LoadUniFormHelper(AsTag):
    name = 'load_uni_form_helper'
    options = Options(
        Argument('importpath', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=True)
    )

    def get_value(self, context, importpath):
        parts = importpath.split('.')
        return getattr(import_module('.'.join(parts[:-1])), parts[-1])

register.tag(LoadUniFormHelper)