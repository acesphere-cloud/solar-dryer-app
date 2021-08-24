import pytest

from .models import Crop, Coefficient
from .tests.factories import CropFactory, CoefficientFactory


@pytest.fixture
def crop() -> Crop:
    return CropFactory()


@pytest.fixture
def coefficient() -> Coefficient:
    return CoefficientFactory()


@pytest.fixture
def default_crop() -> Crop:
    """
    Set Tea as the default crop.
    """
    try:
        # Check whether Tea Object exists in Crop Model
        crop = Crop.objects.get(name="Tea")
    except Crop.DoesNotExist:
        crop_data = {}
        crop_data["name"] = "Tea"
        crop_data["initial_moisture"] = "69"
        crop_data["final_moisture"] = "3"
        crop_data["bulk_density"] = "700"
        crop = Crop.objects.create(**crop_data)
    return crop


@pytest.fixture
def random_crops() -> Crop:
    for _ in range(5):
        CropFactory()
    queryset = Crop.objects.all()
    return queryset
