from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo

from .published import PublishedRel
from .venue import Venue


class Paper(StructuredNode):
    id = StringProperty(required=True)
    key = StringProperty(required=True)
    name = StringProperty(required=True)
    type = StringProperty()
    url = StringProperty()
    ee = StringProperty()
    num_of_authors = IntegerProperty()
    year = IntegerProperty()

    venue = RelationshipTo("Venue", "PUBLISHED AT", model=PublishedRel)
