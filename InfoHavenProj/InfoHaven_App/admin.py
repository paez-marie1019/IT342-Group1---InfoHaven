from django.contrib import admin
from .models import Member
from .models import Book
from .models import BorrowingRecord

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ('Member_ID', 'Fname', 'Lname', 'Password', 'Contact_Details','Email','Type')
    list_filter = ('Member_ID',)
admin.site.register(Member, MemberAdmin)

class BookAdmin(admin.ModelAdmin):
     list_display = ('book_id', 'author_id', 'title', 'summary', 'author', 'publisher','classification','date_published','isbn','status','borrower')
     list_filter = ('book_id',)
admin.site.register(Book, BookAdmin)

class BorrowingRecordAdmin(admin.ModelAdmin):
     list_display = ('Record_ID', 'book_id', 'Member_ID', 'date_borrowed', 'return_date', 'date_returned', 'isReturned', 'penalty')
     list_filter = ('Record_ID',)
admin.site.register(BorrowingRecord, BorrowingRecordAdmin)
