"""Used by Django admin application to get a list of registered models.

To register a model:

from myapp.models import YourModel
admin.site.register(YourModel)
"""

from django.contrib import admin
from cmoapp import models
import inspect

for name,obj in inspect.getmembers(models,inspect.isclass):
    admin.site.register(obj)

