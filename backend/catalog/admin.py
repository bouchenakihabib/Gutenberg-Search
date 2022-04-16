from django.contrib import admin
from .models import Book

# Register your models here.
admin.site.site_title = 'Gutemberg-Search'
admin.site.site_header = 'Gutemberg-Search'
admin.site.admin_name = 'Gutemberg-Search'
admin.site.index_title = 'Admin'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'download_url')
    list_filter = ('language',)
    search_fields = ('title',)