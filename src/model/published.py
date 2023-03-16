from neomodel import (
    StructuredRel,
    IntegerProperty,
)


class PublishedRel(StructuredRel):
    year = IntegerProperty()