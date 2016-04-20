from time import time
from uuid import uuid4, UUID
from .. import exceptions


def create_id():
    return str(uuid4())


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
    if entity:
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
            if propname in ("name", "id") and propname in self._h5obj.attrs:
                raise AttributeError("can't set attribute")
            if value is None:
                if propname == "type":
                    raise AttributeError("type can't be None")
                # Can't set H5Py attribute to None
                # Deleting will return None on get
                del self._h5obj.attrs[propname]
            else:
                self._h5obj.attrs[propname] = value

        def deleter(self):
            del self._h5obj.attrs[propname]

        return property(fget=getter, fset=setter, fdel=deleter)

    for attr in attributes:
        setattr(cls, attr, makeprop(attr))


def create_container_methods(cls, childclass):
    iddict = "_{}s_id".format(childclass)
    namedict = "_{}s_id".format(childclass)
    h5cont = "_{}_group".format(childclass)
    objlist = "_{}s_list".format(childclass)

    def idgetter(self, id_):
        return getattr(self, iddict).get(id_)

    def namegetter(self, name):
        return getattr(self, namedict).get(name)

    def posgetter(self, pos):
        return getattr(self, objlist)[pos]

    def adder(self, item):
        getattr(self, iddict)[item.id] = item
        getattr(self, namedict)[item.name] = item
        getattr(self, objlist).append(item)

    def deleter(self, id_):
        name = getattr(self, iddict)[id_].name
        del getattr(self, h5cont)[name]
        del getattr(self, iddict)[id_]
        del getattr(self, namedict)[name]

    def counter(self):
        return len(getattr(self, h5cont))

    setattr(cls, "_get_{}_by_id".format(childclass), idgetter)
    setattr(cls, "_get_{}_by_name".format(childclass), namegetter)
    setattr(cls, "_get_{}_by_pos".format(childclass), posgetter)
    setattr(cls, "_add_{}".format(childclass), adder)
    setattr(cls, "_delete_{}_by_id".format(childclass), deleter)
    setattr(cls, "_{}_count".format(childclass), counter)

