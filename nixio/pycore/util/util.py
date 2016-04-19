from time import time
from uuid import uuid4, UUID
from .. import exceptions


def create_id():
    return uuid4()


def check_name(name):
    return "/" not in name


def sanitize_name(name):
    return name.replace("/", "_")


def sanitize_unit(unit):
    # TODO: Fix unicode char for py2
    return unit.replace("mu", "u").replace("μ", "u")


def is_uuid(id_):
    try:
        UUID(id_)
        return True
    except ValueError:
        return False


def check_entity_name_and_type(name, type_):
    check_entity_name(name)
    check_entity_type(type_)


def check_entity_type(type_):
    if not type_:
        raise ValueError("String provided for entity type is empty!")


def check_entity_name(name):
    if not name:
        raise ValueError("String provided for entity name is empty!")
    if not check_name(name):
        raise ValueError("String provided for entity name is invalid!")


def check_empty_str(string, field_name):
    if not string:
        raise ValueError("String provided is empty! {}".format(field_name))


def check_name_or_id(name_or_id):
    if not name_or_id:
        raise ValueError("String provided for entity name is empty!")


def check_entity_input(entity, raise_exception=True):
    if entity and entity.is_valid_entity():
        return True
    if raise_exception:
        raise exceptions.UninitializedEntity()
    return False


def nowstr():
    return str(int(time()))


def create_h5props(cls, attributes):

    def makeprop(propname):
        def getter(self):
            return self._h5obj.attrs.get(propname)

        def setter(self, value):
            self._h5obj.attrs.modify(propname, value)
        return property(fget=getter, fset=setter)

    for attr in attributes:
        setattr(cls, attr, makeprop(attr))

