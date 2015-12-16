from django.db.models import Model, CharField, ManyToManyField
from django.db.models.fields.related import RelatedField


class Spell(Model):
        name = CharField(unique=True, max_length=255)

        # classes = ManyToManyField("Class")
        # domains = ManyToManyField("Domain")
        # descriptors = ManyToManyField("Descriptor")
        # school = RelatedField("School")
        # subschool = ManyToManyField("SubSchool")

        components = CharField(max_length=255)
        casting_time = CharField(max_length=255)
        cost = CharField(max_length=255)
        duration = CharField(max_length=255)
        item = CharField(max_length=255)
        refdoc = CharField(max_length=255)
        saveinfo = CharField(max_length=255)
        spell_resistance = CharField(max_length=255)
        targetarea = CharField(max_length=255)


class School(Model):
    name = CharField(unique=True, max_length=255)


class SubSchool(Model):
    name = CharField(unique=True, max_length=255)

#
# class Descriptor(Model):
#     name = CharField(unique=True)
#
#
# class Domain(Model):
#     name = CharField(unique=True)
#
#
# class Class(Model):
#     MAGIC_TYPES = (('arcane', 'arcane'), ('divine', 'divine'))
#
#     name = CharField(unique=True)
#     magic_type = CharField(choices=MAGIC_TYPES)
