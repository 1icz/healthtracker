from django.contrib import admin
from .models import Measurement

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'systolic', 'diastolic', 'pulse')
    list_filter = ('user', 'date')
    search_fields = ('note',)