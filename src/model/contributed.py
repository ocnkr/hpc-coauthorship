from neomodel import (
    StructuredRel,
    IntegerProperty,
)


class ContributedRel(StructuredRel):
    contribution = IntegerProperty()