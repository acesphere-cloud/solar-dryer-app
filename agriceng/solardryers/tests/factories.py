from agriceng.solardryers.models import Dryer, Note
from factory import Faker, Iterator, SubFactory, RelatedFactory
from factory.django import DjangoModelFactory, ImageField

sizes = [i[0] for i in Dryer.SIZE_CHOICES]

versions = [i[0] for i in Dryer.VERSION_CHOICES]


class DryerFactory(DjangoModelFactory):
    size = Iterator(sizes)
    version = Iterator(versions)
    diagram = ImageField()
    construct = ImageField()
    variation = ImageField()

    class Meta:
        model = Dryer
        django_get_or_create = ["size", "version"]


class NoteFactory(DjangoModelFactory):
    note = Faker("bothify", text='##: ?????? Random Note ??####???????? #?#?#')
    dryer = SubFactory(DryerFactory)

    class Meta:
        model = Note
        django_get_or_create = ["note", ]


class NoteFactory2(DjangoModelFactory):
    note = Faker("bothify", text='##: ?????? Random Note ??####???????? #?#?#')
    dryer = RelatedFactory(DryerFactory)

    class Meta:
        model = Note
        django_get_or_create = ["note", ]
