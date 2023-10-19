from django import forms
from .models import Book

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'classification', 'date_published', 'isbn', 'status']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  