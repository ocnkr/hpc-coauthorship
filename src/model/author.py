from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    ArrayProperty,
    Relationship,
    RelationshipTo,
)

from .coauthorship import CoauthorRel
from .attended import AttendedRel
from .contributed import ContributedRel
from .venue import Venue
from .paper import Paper


class Author(StructuredNode):
    pid = StringProperty(unique_index=True)
    name = StringProperty(required=True)
    scholar_url = StringProperty()
    number_of_papers = IntegerProperty()
    number_of_coauthors = IntegerProperty()
    citation = IntegerProperty()
    affiliations = ArrayProperty(StringProperty())
    awards = ArrayProperty(StringProperty())

    coauthor = Relationship("Author", "COAUTHORED WITH", model=CoauthorRel)
    venue = RelationshipTo("Venue", "ATTENDED TO", model=AttendedRel)
    paper = RelationshipTo("Paper", "CONTRIBUTED TO", model=ContributedRel)

    def asdict(self):
        return {
            "pid": self.pid,
            "name": self.name,
            "number_of_papers": self.number_of_papers,
            "number_of_coauthors": self.number_of_coauthors,
        }
