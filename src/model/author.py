from enum import unique
from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    IntegerProperty,
    ArrayProperty,
    Relationship,
)

from .paper import PaperRel
from .venue import Venue


class Author(StructuredNode):
    pid = StringProperty(unique_index=True)
    name = StringProperty(required=True)
    scholar_url = StringProperty()
    number_of_papers = IntegerProperty()
    number_of_coauthors = IntegerProperty()
    citation = IntegerProperty()
    affiliations = ArrayProperty(StringProperty())
    awards = ArrayProperty(StringProperty())

    coauthor = Relationship("Author", "COAUTHOR", model=PaperRel)
    venue = Relationship("Venue", "PUBLISHED AT", model=PaperRel)
