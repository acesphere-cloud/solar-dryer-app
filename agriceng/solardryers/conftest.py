import pytest

from .models import Dryer, Note
from .tests.factories import DryerFactory, NoteFactory, NoteFactory2


@pytest.fixture
def dryer() -> Dryer:
    return DryerFactory()


@pytest.fixture
def note() -> Note:
    return NoteFactory()

@pytest.fixture
def note2() -> Note:
    return NoteFactory2()


@pytest.fixture
def default_note(dryer) -> Note:
    """
    Set Tea as the default crop.
    """
    try:
        default_note = Note.objects.get(note='The quick brown dog jumps over the lazy foxes')
    except Note.DoesNotExist:
        note_data = {
            "note": 'The quick brown dog jumps over the lazy foxes',
            "dryer": dryer,
        }
        default_note = Note.objects.create(**note_data)
    return default_note


@pytest.fixture
def random_notes() -> Note:
    for _ in range(5):
        NoteFactory()
    queryset = Note.objects.all()
    return queryset


@pytest.fixture
def random_dryers() -> Dryer:
    for _ in range(5):
        DryerFactory()
    queryset = Dryer.objects.all()
    return queryset

