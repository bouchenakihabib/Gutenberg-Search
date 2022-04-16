from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.ListField(read_only=True)
    bookshelves = serializers.ListField(read_only=True)

    class Meta:
        model = Book
        exclude = ('jaccard_calculated', 'keywords')


class SearchQuerySerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    advanced = serializers.BooleanField(required=False, allow_null=True, default=False)


class AutoCompleteSerializer(serializers.Serializer):
    q = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")