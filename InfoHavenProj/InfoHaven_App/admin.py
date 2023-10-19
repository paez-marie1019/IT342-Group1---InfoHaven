from django.contrib import admin
from .models import Member
from .models import Book

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ('Member_ID', 'Fname', 'Lname', 'Password', 'Contact_Details','Email','Type')
    list_filter = ('Member_ID',)
admin.site.register(Member, MemberAdmin)

class BookAdmin(admin.ModelAdmin):
     list_display = ('book_id', 'author_id', 'title', 'author', 'publisher','classification','date_published','isbn','status')
     list_filter = ('book_id',)
admin.site.register(Book, BookAdmin)
