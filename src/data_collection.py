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
            # connect the paper to venue
            paper_node.venue.connect(venue_node, {"year": paper["info"]["year"]})
            if "authors" not in paper["info"]:
                continue
            # get the author information for the paper
            authors = paper["info"]["authors"]["author"]
            # some author information is not stored as a list
            if not isinstance(authors, list):
                authors = [authors]
            # store the number of authors of a paper
            paper_node.num_of_authors = len(authors)
            paper_node.save()
            # iterate over authors
            for i in range(len(authors)):
                pid = authors[i]["@pid"]
                name = authors[i]["text"]
                # create author
                author1_node = Author.get_or_create({"pid": pid, "name": name})[0]
                # connect author and venue
                author1_node.paper.connect(paper_node, {"contribution": i + 1})
                if len(authors) > i + 1:
                    # TODO: no need to this for loop
                    for j in range(i + 1, len(authors)):
                        pid = authors[j]["@pid"]
                        name = authors[j]["text"]
                        # create the other author
                        author2_node = Author.get_or_create({"pid": pid, "name": name})[
                            0
                        ]
                        # connect that author to the paper
                        author2_node.paper.connect(paper_node, {"contribution": j + 1})

    file = open(data, "r")
    for line in file.readlines():
        venue_info = line.split(",")
        venue_key = venue_info[2]
        venue_name = venue_info[0]
        venue_type = venue_info[1]
        venue_link = venue_info[3]
        # skip the conferences that are not directly HPC related
        if venue_type == "RC":
            continue

        # create Venue object
        venue_node = Venue.get_or_create(
            {"key": venue_key, "name": venue_name, "type": venue_type}
        )[0]
        # sleep between 1-2 seconds not to get recaptcha
        sleep(randint(60, 120))
        print("{} is started".format(venue_link + "&format=json"))
        # gets the first 1000 papers
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
    return


if __name__ == "__main__":
    main()
