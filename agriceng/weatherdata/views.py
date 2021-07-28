from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import LocationForm
from .weather import WeatherAPIMixin


# class WeatherDataView(WeatherAPIMixin, TemplateView, FormView):
#     template_name = "pages/weather.html"
#     model = Category, Page
#     form_class = LocationForm
#
#     def get_context_data(self, category_name_slug, **kwargs):
#         try:
#             category = Category.objects.get(slug=category_name_slug)
#             pages = Page.objects.filter(category=category).order_by('-views')
#         except Category.DoesNotExist:
#             category = None
#             pages = None
#         kwargs['category'] = category
#         kwargs['pages'] = pages
#         if 'form' not in kwargs:
#             kwargs['form'] = self.get_form()
#         return kwargs
#
#     def form_invalid(self, category_name_slug, query):
#         return self.render_to_response(self.get_context_data(
#             category_name_slug, form=query))
#
#     def form_valid(self, category_name_slug, query):
#         return self.render_search_response(self.get_context_data(
#             category_name_slug, form=query))
#
#     def post(self, request, *args, **kwargs):
#         category_name_slug = kwargs['category_name_slug']
#         query = self.get_form()
#         if query.is_valid():
#             return self.form_valid(category_name_slug, query)
#         else:
#             return self.form_invalid(category_name_slug, query)

