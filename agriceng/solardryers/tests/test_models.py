import pytest

from agriceng.solardryers.models import Dryer, Note

pytestmark = pytest.mark.django_db


class TestDryerModel:
    def test_model_ordering(self, random_dryers):
        assert str(random_dryers[0]) >= str(random_dryers[1])

    def test_dryer_directory(self, dryer: Dryer):
        # Check whether image is uploaded to correct directory in MEDIA_PATH
        directory = 'dryers/{0}/{1}/'.format(dryer.size, dryer.version)
        path_directory = dryer.diagram.path[-24:-11]
        assert path_directory == directory

    def get_size(self, dryer: Dryer):
        # Check whether get size function returns dryer size
        assert dryer.get_size == dryer.size

    def get_version(self, dryer: Dryer):
        # Check whether get version function returns dryer function
        assert dryer.get_version == dryer.version


class TestNoteModel:
    def test_model_ordering(self, random_notes):
        assert str(random_notes[0].dryer) <= str(random_notes[1].dryer)

    def test_note_remove_spaces(self, note: Note):
        string_with_spaces = '  a3dSWfwer213rsd  we are kajsdUHASHId   '
        note.note = string_with_spaces
        note.save()
        assert note.note == 'a3dSWfwer213rsd  we are kajsdUHASHId'
