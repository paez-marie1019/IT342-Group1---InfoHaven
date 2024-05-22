from django import forms
from .models import Book
from .models import Member

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'publisher', 'classification', 'date_published', 'isbn', 'status']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  
        
class BookSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search for books')

class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['Fname', 'Lname','Password', 'Email', 'Contact_Details']
