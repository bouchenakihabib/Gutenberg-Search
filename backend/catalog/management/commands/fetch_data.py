"""
Script for Executions
run:
./manage.py fetch_data
./manage.py fetch_data [--n int]
./manage.py fetch_data --n 5
"""
from django.core.management import BaseCommand
from django.conf import settings
from catalog.scraping import get_books, gutenberg_to_dict
from catalog.models import Book, Keyword


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Collect Books from gutenberg.org"

    def add_arguments(self, parser):
        parser.add_argument(
            '--n',
            type=int,
            default=10,
            help='Number of books to collect',
        )

    def handle(self, *args, **options):
        g_books = get_books()
        i = 0
        for x in range(0, min(settings.MAX_BOOKS_NUMBER, options['n'])):
            i += 1
            try:
                b_dict = next(g_books)
                if not Book.objects.filter(gutenbergID=b_dict.get('id')).exists():
                    b_dict = gutenberg_to_dict(b_dict)
                    if b_dict.get('keywords'):
                        b = Book(**b_dict)
                        b.save()
                        for y in b_dict.get('keywords'):
                            if not Keyword.objects.filter(keyword=y['keyword']).exists():
                                kw = Keyword(keyword=y['keyword'],
                                             books=[{
                                                 'book_gutenbergID': b_dict['gutenbergID'],
                                                 'occurrence_number': y['occurrence_number'],
                                             }])
                                kw.save()
                            else:
                                kw = Keyword.objects.filter(keyword=y['keyword'])
                                for obj in kw[:1]:
                                    obj.books.append({
                                        'book_gutenbergID': b_dict['gutenbergID'],
                                        'occurrence_number': y['occurrence_number'],
                                    })
                                    obj.save()
                        print(i, ' - ', 'Indexed', b.gutenbergID, b.title)
                    else:
                        print(i, ' - ', b_dict.get('id'), 'empty keywords')
                else:
                    print(i, ' - ', b_dict.get('id'), 'already exists')
            except GeneratorExit:
                pass