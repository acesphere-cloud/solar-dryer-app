from agriceng.area.models import Crop, Coefficient
from factory import Faker
from factory.django import DjangoModelFactory

crops = ('Maize', 'Beans', 'Apples', 'Rice', 'Garlic')


class CropFactory(DjangoModelFactory):
    name = Faker("random_element", elements=crops)
    initial_moisture = Faker("pyint")
    final_moisture = Faker("pyint")
    bulk_density = Faker("pyint")
    created = Faker("date_time")
    modified = Faker("date_time")

    class Meta:
        model = Crop
        django_get_or_create = ["name"]


equations = ([i[0] for i in Coefficient.EQUATION_CHOICES])


class CoefficientFactory(DjangoModelFactory):
    coefficient = Faker("catch_phrase")
    symbol = Faker("suffix_nonbinary")
    equivalent = Faker("pyfloat")
    equation = Faker("random_element", elements=equations)
    created = Faker("date_time")
    modified = Faker("date_time")

    class Meta:
        model = Coefficient
        django_get_or_create = ["coefficient"]
