from django import forms

from .models import Dryer, Note


class DryerForm(forms.ModelForm):

    class Meta:
        model = Dryer
        fields = ('size', 'version', 'diagram', 'construct', 'variation',)


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('note', 'dryer',)
