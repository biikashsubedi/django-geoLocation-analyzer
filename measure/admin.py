from django.contrib import admin
from .models import Measure


# Register your models here.

# class MeasureAdmin(admin.ModelAdmin):
#     list_display = ['location', 'destination', 'distance']
#     list_display_links = ['location', 'destination', 'distance']
#     search_fields = ['location', 'destination', 'distance']


admin.site.register(Measure)
