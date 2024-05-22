from django.contrib.auth.models import User
from django.db import models
from datetime import date

class Member(models.Model):
    
    Member_ID = models.CharField(primary_key=True, unique=True, max_length=50)
    Fname = models.CharField(max_length=50)
    Lname = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Contact_Details = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    Type = models.IntegerField(default=0)  # For member type. 0 for regular members and 1 for Librarian.

    # Function to display the Member_ID instead of object in Django Admin
    def __str__(self):
        return self.Member_ID

class Book(models.Model):
    book_id = models.CharField(primary_key=True, unique=True, max_length=50)
    author_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    date_published = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    status = models.CharField(max_length=50)  
    borrower = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.book_id

class BorrowingRecord(models.Model):
    Record_ID = models.CharField(primary_key=True, unique=True, max_length=50)
    book_id = models.ForeignKey('Book', on_delete=models.PROTECT)
    Member_ID = models.CharField(max_length=50)
    date_borrowed = models.DateField(default=None)
    return_date = models.DateField(default=None)
    date_returned = models.DateField(null=True, blank=True)
    penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    # if book is returned via by admin
    isReturned = models.IntegerField(default=0) 
    # if borrowing record is accepted via by admin
    isAccepted = models.IntegerField(default=0) 
    # if book is being borrow via by user
    isRequested = models.IntegerField(default=0)
    

    def __str__(self):
        return self.Record_ID

    def calculate_money_penalty(self):
        if not self.isReturned and self.return_date:
            days_overdue = (date.today() - self.return_date).days
            if days_overdue > 0:
                self.penalty = days_overdue * 20.00
            else:
                self.penalty = 0.00
        else:
            self.penalty = 0.00

class BorrowRequest(models.Model):
    # Your existing fields
    borrowing_record = models.OneToOneField(BorrowingRecord, null=True, blank=True, on_delete=models.SET_NULL)