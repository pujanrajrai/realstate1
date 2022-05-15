from django.contrib import admin
from .models import PropertyStatus, PropertyCategory, Property, PropertyBookMark, State,Comments

# Register your models here.

admin.site.register(PropertyCategory)
admin.site.register(PropertyStatus)
admin.site.register(Property)
admin.site.register(Comments)
admin.site.register(PropertyBookMark)
admin.site.register(State)
