from django.http import Http404
from typing import List
from .models import Book, Keyword
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.conf import settings
from rest_framework.response import Response
from .serializers import SearchQuerySerializer, BookSerializer, AutoCompleteSerializer
import textdistance
from neo4j import GraphDatabase


def suggest_word(keyword: str) -> str:
    res = Keyword.objects.mongo_find({'keyword': {"$regex": f"^{keyword[0]}.{{2,}}"}})
    best_match = None
    max_score = 0
    for x in res:
        suggested = x['keyword']
        scr = textdistance.levenshtein.normalized_similarity(keyword, suggested)
        if scr > settings.SIMILARITY_THRESHOLD:
            return suggested
        if scr > max_score:
            max_score = scr
            best_match = suggested
    if max_score > settings.SIMILARITY_MIN:
        return best_match


def get_similar_books(gutenbergID) -> List:
    driver = GraphDatabase.driver(f"neo4j://{settings.NEO4J_HOST}:{settings.NEO4J_PORT}",
                                  auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

    def get_connected_nodes(tx, book):
        res = tx.run("""
        MATCH (:Book {gutenbergID : $book})<-[:SIMILAR_TO]-(c:Book)
        RETURN c.gutenbergID AS gutenbergID 
        """, book=book)
        r = []
        for x in res:
            r.append(x.get('gutenbergID'))
        return r

    with driver.session() as session:
        results = session.read_transaction(get_connected_nodes, gutenbergID)
        queryset = Book.objects.filter(gutenbergID__in=results).order_by('-centrality_rank')[
                   :settings.SIMILAR_BOOKS_NUMBER]
        serializer = BookSerializer(queryset, many=True)
    driver.close()
    return serializer.data


class SearchViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SearchQuerySerializer

    def list(self, request):
        serializer = self.serializer_class(data=request.query_params)  # or request.GET
        serializer.is_valid(raise_exception=True)
        keyword = serializer.validated_data.get('keyword')
        is_advanced = serializer.validated_data.get('advanced')
        if not keyword:
            return Response([])
        matched = set()
        if not is_advanced:
            # case keyword
            from .nlp import clean, stem
            keyword_cleaned = stem(clean(keyword))
            res = Keyword.objects.filter(keyword=keyword_cleaned)
            for x in res:
                for y in x.books:
                    matched.add(y['book_gutenbergID'])
        else:
            # case regex
            res = Keyword.objects.mongo_find({'keyword': {"$regex": keyword}})
            for x in res:
                for y in x['books']:
                    matched.add(y['book_gutenbergID'])
        books = Book.objects.filter(gutenbergID__in=list(matched)).order_by('-centrality_rank')[
                :settings.BOOKS_RESULT_NUMBER]
        serializer = BookSerializer(data=books, many=True)
        serializer.is_valid(False)
        if not serializer.data:
            if not is_advanced:
                return Response(suggest_word(keyword) or [])
            else:
                return Response([])
        return Response(serializer.data)


class AutoCompleteViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = AutoCompleteSerializer

    def list(self, request):
        serializer = self.serializer_class(data=request.query_params)  # or request.GET
        serializer.is_valid(raise_exception=True)
        q = serializer.validated_data.get('q')
        if not q:
            return Response([])
        res = Keyword.objects.mongo_find({'keyword': {"$regex": f"^{q}.*$", }}).limit(settings.AUTOCOMPLETE_NUMBER)
        suggestions = []
        for x in res:
            suggestions.append(x['keyword'])
        return Response(suggestions)


class BookViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Book.objects.filter(gutenbergID=pk).first()
        serializer = BookSerializer(queryset)
        if not serializer.data['gutenbergID']:
            raise Http404()
        d = serializer.data
        d['similar_to'] = get_similar_books(serializer.data['gutenbergID'])
        return Response(d)