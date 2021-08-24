import pytest

from agriceng.area.models import Crop, Coefficient

pytestmark = pytest.mark.django_db


def test_crop_model_ordering(random_crops):
    assert str(random_crops[0]) < str(random_crops[1])


def test_coefficient_field_no_capitals_nor_spaces(coefficient: Coefficient):
    string_with_spaces_and_capitals = '  a3dSWfwer213rsd  we are kajsdUHASHId   '
    coefficient.coefficient = string_with_spaces_and_capitals
    coefficient.save()
    assert coefficient.coefficient == 'a3dswfwer213rsd  we are kajsduhashid'
