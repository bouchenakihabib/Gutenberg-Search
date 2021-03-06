from django.core.management import BaseCommand
from neo4j import GraphDatabase
from catalog.models import Book
from django.conf import settings
from catalog.jaccard import calculate_distance


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Calculate Jaccard Graph"

    def handle(self, *args, **options):
        print("Jaccard Graph")
        driver = GraphDatabase.driver(f"neo4j://{settings.NEO4J_HOST}:{settings.NEO4J_PORT}",
                                      auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

        def add_relationship(tx, book1, book2):
            tx.run("""
            MERGE (a:Book {gutenbergID:$book1})
            MERGE (b:Book {gutenbergID:$book2})
            MERGE (a)-[:SIMILAR_TO]->(b)
            MERGE (b)-[:SIMILAR_TO]->(a);
            """, book1=book1, book2=book2)

        books = Book.objects.all().values()
        ll = len(books)
        for i in range(0, ll):
            for j in range(i + 1, ll):
                x = books[i]
                y = books[j]
                score = calculate_distance(x['keywords'], y['keywords'])
                print(score, x['gutenbergID'], y['gutenbergID'])
                if score <= settings.JACCARD_DISTANCE_THETA:
                    with driver.session() as session:
                        session.write_transaction(add_relationship, x['gutenbergID'], y['gutenbergID'])
        driver.close()