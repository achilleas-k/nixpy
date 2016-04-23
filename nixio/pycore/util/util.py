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
        UUID(str(id_))
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


def check_entity_id(id_):
    if not is_uuid(id_):
        raise ValueError("String provided for id is not a valid UUID")


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


def now():
    return int(time())


def create_h5props(cls, attributes, types=None):

    def makeprop(propname, type_):

        def getter(self):
            value = self._h5obj.attrs.get(propname)
            if type_:
                value = type_(value)
            return value

        def setter(self, value):
            if type_ and not isinstance(value, type_):
                raise TypeError("Attribute {} requires type {} but {} "
                                "was provided".format(propname, type_,
                                                      type(value)))
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
            # TODO: Allow deleting attributes?
            # TODO: Do not allow deleting required attributes (name, type, id)
            del self._h5obj.attrs[propname]

        return property(fget=getter, fset=setter, fdel=deleter)

    if types is None:
        types = [None]*len(attributes)
    for attr, type_ in zip(attributes, types):
        setattr(cls, attr, makeprop(attr, type_))


def create_container_methods(cls, chcls, chclsname):
    # TODO: Better exception handling and messages

    if chclsname == "block":
        container = "data"
    else:
        container = chclsname + "s"

    def id_or_name_getter(self, id_or_name):
        if is_uuid(id_or_name):
            for h5obj in self._h5obj[container].values():
                if h5obj.attrs["id"] == id_or_name:
                    break
            else:
                raise ValueError
        else:
            try:
                h5obj = self._h5obj[container][id_or_name]
            except Exception:
                raise ValueError
        return chcls(h5obj)

    def pos_getter(self, pos):
        obj = list(self._h5obj[container].values())[pos]
        return chcls(obj)

    def deleter(self, id_or_name):
        if is_uuid(id_or_name):
            name = id_or_name_getter(self, id_or_name).name
        else:
            name = id_or_name
        try:
            del self._h5obj[container][name]
        except Exception:
            raise ValueError

    def counter(self):
        return len(self._h5obj[container])

    setattr(cls, "_get_{}_by_id".format(chclsname), id_or_name_getter)
    setattr(cls, "_get_{}_by_pos".format(chclsname), pos_getter)
    setattr(cls, "_delete_{}_by_id".format(chclsname), deleter)
    setattr(cls, "_{}_count".format(chclsname), counter)

