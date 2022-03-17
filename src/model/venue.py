from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    IntegerProperty,
    ArrayProperty,
)


class Venue(StructuredNode):
    VENUE_TYPES = {"C": "Conference", "J": "Journal", "RC": "Related Conference"}
    key = StringProperty(unique_index=True)
    name = StringProperty(required=True)
    type = StringProperty(choices=VENUE_TYPES)
    avg_citation_per_paper = IntegerProperty()
    urls = ArrayProperty(StringProperty())
    h_index = ArrayProperty(StringProperty())
