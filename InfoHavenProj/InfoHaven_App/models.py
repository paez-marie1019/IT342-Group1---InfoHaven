from django.contrib.auth.models import User
from django.db import models

class Member(models.Model):
    Member_ID = models.CharField(primary_key=True, unique=True, max_length=50)
    Fname = models.CharField(max_length=50)
    Lname = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Contact_Details = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    Type = models.IntegerField(default=0)  # For member type. 0 for regular members and 1 for Librarian.
    borrowed_books = models.ManyToManyField('Book', blank=True)  # Many-to-many relationship with Book model

    # Function to display the Member_ID instead of object in Django Admin
    def __str__(self):
        return self.Member_ID

class Book(models.Model):
    book_id = models.CharField(primary_key=True, unique=True, max_length=50)
    author_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    date_published = models.DateField()
    isbn = models.CharField(max_length=13)  
    status = models.CharField(max_length=50)  
    borrower = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.book_id
