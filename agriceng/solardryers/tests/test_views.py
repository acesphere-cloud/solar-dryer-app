# import pytest
#
# from django.http import HttpRequest
# from django.test import RequestFactory
#
# from agriceng.area.views import solar_dryer_view
#
# pytestmark = pytest.mark.django_db
#
#
# class SolarDryerViewTest:
#     """
#     TODO:
#         Ensure form error raises Request Timeout when there is no connectivity during
#         API query
#     """
#
#     def test_post_request_timeout(self, request: HttpRequest):
#         return None
#
#     #     def test_form_valid(self, user: User, rf: RequestFactory):
#     #         view = UserUpdateView()
#     #         request = rf.get("/fake-url/")
#     #
#     #
#     #         view.request = request
#     #
#     #         # Initialize the form
#     #         form = UserChangeForm()
#     #         form.cleaned_data = []
#     #         view.form_valid(form)
#     #
#     #         messages_sent = [m.message for m in messages.get_messages(request)]
#     #         assert messages_sent == ["Information successfully updated"]
#
#     #     def test_pdf_form_valid(self, user: User, rf: RequestFactory):
#     #         view = UserUpdateView()
#     #         request = rf.get("/fake-url/")
#     #
#     #
#     #         view.request = request
#     #
#     #         # Initialize the form
#     #         form = UserChangeForm()
#     #         form.cleaned_data = []
#     #         view.form_valid(form)
#     #
#     #         messages_sent = [m.message for m in messages.get_messages(request)]
#     #         assert messages_sent == ["Information successfully updated"]
#
#     def test_get(self, rf: RequestFactory):
#         """
#         Ensure get response successful
#         """
#         # Initiate request
#         request = rf.get("/fake-url/")
#
#         response = solar_dryer_view(request)
#
#         assert response.status_code == 200
