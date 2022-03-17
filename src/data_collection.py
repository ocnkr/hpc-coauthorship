import json, requests
from neomodel import config
from model.author import Author
from model.venue import Venue
from model.paper import PaperRel


def collect_from_venues():
    # TODO (1): Go to each conference.
    # TODO (2): Iteratively create author and venue nodes and add papers as relationships (edges).
    return


def collect_from_authors():
    # TODO (3): Go to each authors' homepage and look at other papers and do the same.
    return


def main():
    config.DATABASE_URL = "bolt://neo4j:1234@localhost:7687"

    # TODO: read from conferences.csv
    # TODO: parse json files until there is no more paper

    # author1 = Author.get_or_create({"pid": "2", "name": "author1"})
    # author2 = Author.get_or_create({"pid": "2", "name": "author1"})
    # venue1 = Venue(name="venue1").save()
    # author3 = Author.nodes.get(pid="2")
    # print(author1 == author2)
    # author2 = Author.nodes.get(name="author2")
    # venue1 = Venue.nodes.get(name="venue1")
    # author1.coauthor.connect(author2, {"key": "paperkey", "title": "papertitle"})
    # author1.venue.connect(venue1, {"key": "paperkey", "title": "papertitle"})
    # author2.venue.connect(venue1, {"key": "paperkey", "title": "papertitle"})
    # for nodes in Author.nodes.all():
    #     nodes.delete()
    # for nodes in Venue.nodes.all():
    #     nodes.delete()
    return


if __name__ == "__main__":
    main()
