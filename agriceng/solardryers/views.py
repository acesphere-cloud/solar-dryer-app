from django.views.generic import ListView

from .models import Dryer, Note


class DryerListView(ListView):
    model = Dryer
    context_object_name = 'dryers'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the notes
        context['notes'] = Note.objects.all()
        return context


dryer_list_view = DryerListView.as_view()
