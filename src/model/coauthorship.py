from neomodel import (
    StructuredRel,
    IntegerProperty,
)


class CoauthorRel(StructuredRel):
    number_of_collabs = IntegerProperty()