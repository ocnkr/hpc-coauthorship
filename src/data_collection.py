import json, requests
from neomodel import config
from random import randint
from time import sleep
from model.author import Author
from model.venue import Venue
from model.paper import Paper
from model.coauthorship import CoauthorRel
from model.published import PublishedRel
from model.contributed import ContributedRel
from model.attended import AttendedRel


def collect_from_venues(data):
    def create_connect_authors(papers, venue_node):
        # TODO (2): Iteratively create author and venue nodes and add papers as relationships (edges).
        for paper in papers:
            # create paper
            ee = ""
            if "ee" in paper["info"]:
                ee = paper["info"]["ee"]
            paper_node = Paper.get_or_create(
                {
                    "id": paper["@id"],
                    "key": paper["info"]["key"],
                    "name": paper["info"]["title"],
                    "url": paper["info"]["url"],
                    "ee": ee,
                    "year": paper["info"]["year"],
                }
            )[0]
            paper_node.venue.connect(venue_node, {"year": paper["info"]["year"]})
            if "authors" not in paper["info"]:
                continue
            authors = paper["info"]["authors"]["author"]
            if not isinstance(authors, list):
                authors = [authors]
            paper_node.num_of_authors = len(authors)
            paper_node.save()
            for i in range(len(authors)):
                pid = authors[i]["@pid"]
                name = authors[i]["text"]
                # create author
                author1_node = Author.get_or_create({"pid": pid, "name": name})[0]
                # connect author and venue
                author1_node.paper.connect(paper_node, {"contribution": i + 1})
                if len(authors) > i + 1:
                    for j in range(i + 1, len(authors)):
                        pid = authors[j]["@pid"]
                        name = authors[j]["text"]
                        author2_node = Author.get_or_create({"pid": pid, "name": name})[
                            0
                        ]
                        author2_node.paper.connect(paper_node, {"contribution": j + 1})

    file = open(data, "r")
    for line in file.readlines():
        venue_info = line.split(",")
        venue_key = venue_info[2]
        venue_name = venue_info[0]
        venue_type = venue_info[1]
        venue_link = venue_info[3]
        if venue_type == "RC":
            continue

        # create Venue object
        venue_node = Venue.get_or_create(
            {"key": venue_key, "name": venue_name, "type": venue_type}
        )[0]
        # gets the first 1000 papers
        sleep(randint(60, 120))
        print("{} is started".format(venue_link + "&format=json"))
        venue_dict = requests.get(venue_link + "&format=json").json()
        total_papers = int(venue_dict["result"]["hits"]["@total"])
        computed = int(venue_dict["result"]["hits"]["@computed"])
        sent = int(venue_dict["result"]["hits"]["@sent"])
        first = int(venue_dict["result"]["hits"]["@first"])
        print(total_papers, computed, sent, first)

        create_connect_authors(venue_dict["result"]["hits"]["hit"], venue_node)

        # read all papers
        for i in range(total_papers // 1000):
            sleep(randint(60, 120))
            req_string = venue_link + "&f={}&format=json".format((i + 1) * 1000)
            print(req_string)
            venue_dict = requests.get(req_string).json()
            total_papers = int(venue_dict["result"]["hits"]["@total"])
            computed = int(venue_dict["result"]["hits"]["@computed"])
            sent = int(venue_dict["result"]["hits"]["@sent"])
            first = int(venue_dict["result"]["hits"]["@first"])
            print(total_papers, computed, sent, first)
            create_connect_authors(venue_dict["result"]["hits"]["hit"], venue_node)

        print("{} is done".format(venue_link + "&format=json"))
    return


def collect_from_authors():
    # TODO (3): Go to each authors' homepage and look at other papers and do the same.
    return


def main():
    config.DATABASE_URL = "bolt://neo4j:1234@localhost:7687"

    collect_from_venues("data\conferences.csv")

    # sleep(randint(60, 120))
    # for i in range(total_papers // 1000):
    #     req_string = "https://dblp.uni-trier.de/search/publ/api?q=stream%3Astreams%2Fconf%2Fics%3A&h=1000&f={}&format=json".format(
    #         (i + 1) * 1000
    #     )
    #     print(req_string)
    #     req = requests.get(req_string)
    #     venue_dict = json.loads(req.text)
    #     total_papers = int(venue_dict["result"]["hits"]["@total"])
    #     computed = int(venue_dict["result"]["hits"]["@computed"])
    #     sent = int(venue_dict["result"]["hits"]["@sent"])
    #     first = int(venue_dict["result"]["hits"]["@first"])
    #     print(total_papers, computed, sent, first)
    # for paper in venue_dict["result"]["hits"]["hit"]:
    #     # create paper link
    #     for i in range(len(paper["info"]["authors"]["author"])):
    #         # author1 = Author.get_or_create()
    #         for j in range(i+1, len(paper["info"]["authors"]["author"])):
    #             # author2 = Author.get_or_create()
    #             # author1.coauthor.connect(author2, {"key": "paperkey", "title": "papertitle"})

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
