from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Dryer, Note
from .forms import DryerForm, NoteForm


@admin.register(Dryer)
class DryerAdmin(admin.ModelAdmin):
    form = DryerForm
    fieldsets = (
        (_('Dryer Name'), {'fields': ('size', 'version')}),
        (_('Schematics'), {'classes': ('extrapretty'), 'fields': ('diagram', 'construct', 'variation', )}),
        (_('Timestamps'), {'classes': ('collapse', ), 'fields': ('created', 'modified')}),
    )
    list_display = ('size', 'version', 'created',)
    list_filter = ('size', 'version',)
    readonly_fields = ('created', 'modified')
    search_fields = ('size', 'version',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    form = NoteForm
    fieldsets = (
        (None, {'fields': ('dryer', 'note',)}),
        (_('Timestamps'), {'classes': ('collapse',), 'fields': ('created', 'modified')}),
    )
    list_display = ('dryer', 'note', 'created', )
    list_filter = ('dryer', )
    readonly_fields = ('created', 'modified')
    search_fields = ('dryer', 'note',)
    date_hierarchy = 'modified'

