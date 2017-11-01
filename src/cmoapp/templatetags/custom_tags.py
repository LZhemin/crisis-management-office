from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.db.models import Model
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.template import Library
from django.forms import BoundField
import json
from datetime import timedelta

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    if isinstance(object, Model):
        return mark_safe(serialize('json', object))
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True

#a tag to render fucking labels because django couldn't provide one
@register.simple_tag
def render_label(obj,**kwargs):
    if isinstance(obj, BoundField):
        content = kwargs.pop('content',None)
        label_suffix = kwargs.pop('label_suffix',None)
        return format_html(obj.label_tag(contents=content,attrs=kwargs,label_suffix=label_suffix))
    raise TypeError("render_label expects a BoundField instance, but supplied obj is instance of "
                    + obj.__class__.__name__)

render_label.is_safe = True

@register.simple_tag
def render_duration(obj, max_days_before_weeks = 14):
    if isinstance(obj, timedelta):
        if(obj.days):
            if(obj.days < max_days_before_weeks):
                output = str(obj.days) + " Days"
            else:
                output = str(int(obj.days/7)) + " Weeks"
        else:
            output = str(int(obj.seconds/60/60)) + " Hours"
        return mark_safe(output)
    raise TypeError("render_duration expects a TimeDelta instance, but supplied obj is instance of "
                    + obj.__class__.__name__)

render_duration.is_safe = True
