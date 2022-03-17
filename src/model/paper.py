from neomodel import (
    StructuredRel,
    StringProperty,
    IntegerProperty,
    ArrayProperty,
)


class PaperRel(StructuredRel):
    key = StringProperty(required=True)
    title = StringProperty(required=True)
    author_pids = ArrayProperty(StringProperty())
    author_names = ArrayProperty(StringProperty())
    year = IntegerProperty()
    url = StringProperty()
