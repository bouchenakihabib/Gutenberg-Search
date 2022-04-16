from django.core.management import BaseCommand
from neo4j import GraphDatabase
from catalog.models import Book
from django.conf import settings


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Calculate Centrality - Betweenness"

    def handle(self, *args, **options):
        print("Betweenness Centrality")
        driver = GraphDatabase.driver(f"neo4j://{settings.NEO4J_HOST}:{settings.NEO4J_PORT}",
                                      auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

        def create_undirected_graph(tx):
            tx.run("""
            CALL gds.graph.create('myBooksGraph', 'Book', {SIMILAR_TO: {orientation: 'NATURAL'}})
            """)

        def remove_undirected_graph(tx):
            tx.run("""
            CALL gds.graph.drop('myBooksGraph')
            """)

        def neo4j_betweenness(tx):
            res = tx.run("""
            CALL gds.betweenness.stream('myBooksGraph')
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).gutenbergID AS gutenbergID, score
            ORDER BY score DESC
            """)
            scores = {}
            for r in res:
                scores[r.get('gutenbergID')] = r.get('score')
            return scores

        try:
            with driver.session() as session:
                session.write_transaction(remove_undirected_graph)
        except Exception as e:
            pass

        with driver.session() as session:
            session.write_transaction(create_undirected_graph)

        with driver.session() as session:
            results = session.read_transaction(neo4j_betweenness)
            for k, v in results.items():
                print(k, v)
                b = Book.objects.filter(gutenbergID=k).first()
                b.centrality_rank = v
                b.save()
               

        driver.close()