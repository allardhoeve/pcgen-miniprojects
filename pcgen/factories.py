import factory
from pcgen.models import Class, Domain, SubSchool, School, Spell


class SpellFactory(factory.DjangoModelFactory):
    class Meta:
        model = Spell

    school = factory.SubFactory(SchoolFactory)
    subschool = factory.SubFactory(SubSchoolFactory)



class SchoolFactory(factory.DjangoModelFactory):
    class Meta:
        model = School

    name = lambda n: "school%n" % n


class SubSchoolFactory(factory.DjangoModelFactory):
    class Meta:
        model = SubSchool

    name = lambda n: "subschool%n" % n
    school = factory.SubFactory(SchoolFactory)
