"""Used by Django admin application to get a list of registered models.

To register a model:

from myapp.models import YourModel
admin.site.register(YourModel)
"""

from django.contrib import admin
from django.db.models import Model
from cmoapp import models
import inspect

try:
    for name,obj in inspect.getmembers(models,inspect.isclass):
        if(isinstance(obj, Model)):
            admin.site.register(obj)
except(TypeError):
    print("Obj Throwing error : %s " % obj)
