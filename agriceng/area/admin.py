from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Crop, Coefficient
from .forms import CropForm, CoefficientForm


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    form = CropForm
    fieldsets = (
        (_('Crop Moisture & Density'), {'fields': ('name', 'initial_moisture', 'final_moisture', 'bulk_density')}),
        (_('Timestamps'), {'classes': ('collapse',), 'fields': ('created', 'modified')}),
    )
    list_display = ('name', 'initial_moisture', 'final_moisture', 'bulk_density',)
    list_filter = ('name', 'bulk_density',)
    readonly_fields = ('created', 'modified')
    search_fields = ('name',)


@admin.register(Coefficient)
class CoefficientAdmin(admin.ModelAdmin):
    form = CoefficientForm
    fieldsets = (
        (_('Equation Coefficients'), {'fields': ('equation', 'coefficient', 'symbol', 'value')}),
        (_('Timestamps'), {'classes': ('collapse', ), 'fields': ('created', 'modified')}),
    )
    list_display = ('equation', 'coefficient', 'symbol', 'value')
    list_display_links = ('coefficient',)
    list_filter = ('equation',)
    readonly_fields = ('created', 'modified')
    search_fields = ('equation', 'coefficient',)
