from uuid import uuid4, UUID


def create_id():
    return uuid4()


def check_name(name):
    return "/" not in name


def sanitize_name(name):
    return name.replace("/", "_")


def sanitize_unit(unit):
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
