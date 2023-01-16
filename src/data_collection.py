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
from neomodel import db


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


# TODO (optional): Go to each authors' homepage and look at other papers and do the same.
def collect_from_authors():
    return


def main():
    config.DATABASE_URL = "bolt://neo4j:1234@localhost:7687"

    # collect_from_venues("data\conferences.csv")

    # connect authors
    # query = "MATCH (a1:Author)-[r1:`CONTRIBUTED TO`]->(p:Paper)<-[r2:`CONTRIBUTED TO`]-(a2:Author) WHERE p.year <= 1985 and id(a1) < id(a2) with a1, a2, collect(p) as copapers MERGE (a1) - [r3:`COAUTHORED WITH` {count: size(copapers)}] - (a2) Return *"
    # results, meta = db.cypher_query(query)

    # export all data
    # export_all = "CALL apoc.export.graphml.all('hpc_coauthor_all.graphml', {})"
    # results, meta = db.cypher_query(export_all)

    # export only coauthorship network
    # export_to_file = "MATCH (p1:Author) "
    # + "OPTIONAL MATCH (p1)-[r:`COAUTHORED WITH`]-(p2) "
    # + "WITH collect(DISTINCT p1) AS author1, collect(DISTINCT p2) AS author2, collect(DISTINCT r) AS coauthor "
    # + "CALL apoc.export.graphml.data(author1+author2, coauthor, 'hpc_coauthor.graphml', {}) "
    # + "YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data "
    # + "RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data "
    # results, meta = db.cypher_query(export_to_file)

    # years = ["1985", "1990", "1995", "2000", "2005", "2010", "2015", "2022"]
    # for year in years:
    #     export_to_file = (
    #         "WITH 'Match (n:Author) -[:`CONTRIBUTED TO`] - (p:Paper) - [:`CONTRIBUTED TO`] - (n2:Author) where p.year <= "
    #         + year
    #         + " With collect(distinct n) as first, collect(distinct n2) as second Match (n:Author) - [r:`COAUTHORED WITH`] - (n2:Author) where n in first and n2 in second Return distinct n,r,n2' AS query "
    #         + "CALL apoc.export.graphml.query(query, 'hpc_coauthor_"
    #         + year
    #         + ".graphml', {}) "
    #         + "YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data "
    #         + "RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data "
    #     )

    # all co-authorship networks
    # for year in range(1985, 2023):
    #     connect_authors = (
    #         "MATCH (a1:Author)-[r1:`CONTRIBUTED TO`]->(p:Paper)<-[r2:`CONTRIBUTED TO`]-(a2:Author) WHERE p.year <= "
    #         + str(year)
    #         + " and id(a1) < id(a2) with a1, a2, collect(p) as copapers MERGE (a1) - [r3:`COAUTHORED WITH` {count: size(copapers)}] - (a2) Return *"
    #     )
    #     results, meta = db.cypher_query(connect_authors)

    # export_to_file = (
    #     "WITH 'MATCH q = (a:Author) - [:`CONTRIBUTED TO`] - (p:Paper) WHERE p.year <= "
    #     + str(year)
    #     + " OPTIONAL MATCH (a:Author) - [r:`COAUTHORED WITH`] - (a2:Author) return DISTINCT a,r,a2' as query CALL apoc.export.graphml.query(query, 'hpc_coauthor_"
    #     + str(year)
    #     + ".graphml', {})"
    #     + " YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data"
    #     + " RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;"
    # )
    # results, meta = db.cypher_query(export_to_file)

    # export_to_file = (
    #     "MATCH (p1:Author) - [:`CONTRIBUTED TO`] - (p:Paper) "
    #     + "WHERE p.year <= "
    #     + str(year)
    #     + " "
    #     + "OPTIONAL MATCH (p1)-[r:`COAUTHORED WITH`]-(p2) "
    #     + "WITH collect(DISTINCT p1) AS author1, collect(DISTINCT p2) AS author2, collect(DISTINCT r) AS coauthor "
    #     + "CALL apoc.export.graphml.data(apoc.coll.toSet(author1 + author2), coauthor, 'hpc_coauthortest"
    #     + str(year)
    #     + ".graphml', {}) "
    #     + "YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data "
    #     + "RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data "
    # )
    # results, meta = db.cypher_query(export_to_file)

    # delete_rel = "MATCH ()-[r:`COAUTHORED WITH`]-() DELETE r"
    # results, meta = db.cypher_query(delete_rel)

    # GET THE MOST PUBLISHED VALUE
    # "MATCH (a:Author) - [r:`CONTRIBUTED TO`] -> (p: Paper) - [r2: `PUBLISHED AT`] -> (v:Venue)"
    # + " WITH a, v, count(p) AS paper_count "
    # + " ORDER BY paper_count DESC"
    # + " RETURN a, collect(v)[0] AS most_venue, max(paper_count) AS contribution_count"

    # CONNECT AUTHORS TO VENUES
    # query = "MATCH (a:Author)-[:`CONTRIBUTED TO`]->(p:Paper)-[:`PUBLISHED AT`]->(v:Venue) WITH a, v, collect(p) as papers MERGE (a) - [r3:`ATTENDED TO` {count: size(papers)}] - (v) RETURN *"
    # results, meta = db.cypher_query(query)

    export_to_file = "WITH 'MATCH (a:Author)-[r:`ATTENDED TO`]->(v:Venue) WITH a, r, apoc.agg.maxItems(v, r.count) AS mv_agg RETURN a, r, mv_agg.items[0] AS max_venue' as query CALL apoc.export.graphml.query(query, 'author-venue2.graphml', {}) YIELD file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data RETURN file, source, format, nodes, relationships, properties, time, rows, batchSize, batches, done, data;"
    results, meta = db.cypher_query(export_to_file)
    return


if __name__ == "__main__":
    main()
