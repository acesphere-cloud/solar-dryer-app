"""
Module for all Form Tests.
"""
import pytest
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile

from agriceng.solardryers.forms import DryerForm, NoteForm
from agriceng.solardryers.models import Dryer, Note

pytestmark = pytest.mark.django_db


class TestDryerForm:
    """
    Test class for all tests related to the UserCreationForm
    """

    def test_dryer_form_unique_constraint(self, dryer: Dryer):
        """
        Tests DryerForm Form's unique validator functions correctly by testing:
            1) A new dryer with an existing dryer size and version cannot be added.
            2) Only 1 error is raised by the DryerForm Form
            3) The desired error message is raised
        """

        # The dryer already exists,
        # hence cannot be created.

        data = {
            "size": dryer.size,
            "version": dryer.version,
        }
        file_data = {
            "diagram": dryer.diagram,
            "construct": dryer.construct,
            "variation": dryer.variation,
        }

        form = DryerForm(data, file_data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "__all__" in form.errors
        assert form.errors["__all__"][0] == _("Dryer with this Size and Version already exists.")

    def test_diagram_field_output_type(self):
        """
        Tests DryerForm Form's type validator functions correctly by testing:
            1) A new dryer with a fake image diagram cannot be added.
            2) Only 1 error is raised by the DryerForm Form
            3) The desired error message is raised
        """
        # The diagram entry is a non-image type,
        # hence cannot be created.
        data = {
            "size": Dryer.LARGE,
            "version": Dryer.SIMPLE,
        }
        file_data = {
            "diagram": SimpleUploadedFile('fake_image_name.jpg', b'fake image data')
        }

        form = DryerForm(data, file_data)

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "diagram" in form.errors
        assert form.errors["diagram"][0] == _(
            "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
        )


class TestNoteForm:
    """
    Test class for all tests related to the UserCreationForm
    """

    def test_note_validation_error_msg(self, note: Note):
        """
        Tests NoteForm Form's unique validator functions correctly by testing:
            1) A new user with an existing username cannot be added.
            2) Only 1 error is raised by the NoteForm Form
            3) The desired error message is raised
        """

        # The Note exceeds the permissible length,
        # hence cannot be created.
        form = NoteForm(
            {
                "note": "One efficiency report from the 1960s stated that in one period of 3 hours 50 minutes, "
                        "the computer scanned more than seven million messages of about 500 characters each, "
                        "examining them for any of 7000 different words or phrases of interest to the national agency.",
                "dryer": note.dryer,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "note" in form.errors
        assert "Ensure this value has at most 256 characters" in form.errors["note"][0]
