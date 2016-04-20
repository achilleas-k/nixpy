class DuplicateName(Exception):

    def __init__(self, caller, *args, **kwargs):
        self.message = ("Duplicate name - "
                        "names have to be unique for a given "
                        "entity type & parent. ({})").format(caller)
        super(DuplicateName, self).__init__(self.message, *args, **kwargs)


class UninitializedEntity(Exception):

    def __init__(self, *args, **kwargs):
        self.message = "The Entity being accessed is uninitialized or empty."
        super(UninitializedEntity, self).__init__(self.message, *args, **kwargs)

