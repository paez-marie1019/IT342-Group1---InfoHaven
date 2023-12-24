from datetime import date, timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import BorrowingRecord, Member, Book
from django.utils import timezone
from .forms import BookForm
from .forms import BookUpdateForm
from .forms import BookSearchForm
from django.contrib.auth.decorators import login_required
from .forms import UpdateMemberForm
from django.http import HttpResponseRedirect
from datetime import datetime

# Create your views here.
def home(request):
    return render(request,"InfoHaven_App/introduction.html")

def register(request):    
    # Checks if the HTTP request method is POST.
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['fname']
        last_name = request.POST['lname']

        # Check if the username or email already exists in the Member table
        if Member.objects.filter(Member_ID=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('Register')
        if Member.objects.filter(Email=email).exists():
            messages.error(request, "Email address already registered. Please use a different email.")
            return redirect('Register')

        # Create a new Member
        member = Member(Member_ID=username, Email=email, Password=password, Fname=first_name, Lname=last_name, Type=0)
        member.save()

        # Display a success message
        messages.success(request, "Successfully Registered!")

        # Redirect to the desired page after successful registration
        return redirect('Login')  # Change 'Login' to the appropriate URL name

    return render(request, "InfoHaven_App/Register.html")

def login(request):
    # Checks if the HTTP request method is POST.
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Retrieve the user based on the Member_ID
            member = Member.objects.get(Member_ID=username)

            # Check if the provided password matches the user's password
            if member.Password == password:
                # Store the ID and Fname in the session
                request.session['member_id'] = member.Member_ID
                request.session['member_fname'] = member.Fname
                request.session['member_type'] = member.Type

                # Redirect to the start page
                if member.Type == 0:
                    return redirect('Start_Logged')
                else:
                    return redirect('DashboardAdmin')
                   

            else:
                # Display an error message for incorrect password
                messages.error(request, "Incorrect Password")
                return redirect('Login')

        except Member.DoesNotExist:
            # Display an error message for an unknown username
            messages.error(request, "Username not found")
            return redirect('Login')

    return render(request, "InfoHaven_App/Login.html")

def logout(request):
     # Clear the session variables
    if 'member_id' in request.session:
        del request.session['member_id']
    if 'member_fname' in request.session:
        del request.session['member_fname']

    return render(request,"InfoHaven_App/start.html")

def start(request):
    return render(request,"InfoHaven_App/start.html")

def start_logged(request):
    return render(request,"InfoHaven_App/start_logged.html")

def dashboard(request):
    # Query the database to get a list of books
    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, 'InfoHaven_App/Dashboard.html', context)  

def dashboard_admin(request):
    # Query the database to get a list of books
    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, 'InfoHaven_App/Dashboard-admin.html', context) 

def dashboard_guest(request):
    # Query the database to get a list of books
    books = Book.objects.all()

    context = {
        'books': books,
    }

    return render(request, 'InfoHaven_App/DashboardGuest.html', context) 

def update_book(request, book_id):
    book = Book.objects.get(book_id=book_id)

    if request.method == 'POST':
        form = BookUpdateForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('DashboardAdmin')  

    else:
        form = BookUpdateForm(instance=book)

    context = {
        'form': form,
        'book': book,
    }

    return render(request, 'InfoHaven_App/update_book.html', context)

def delete_book(request, book_id):
    book = Book.objects.get(book_id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('DashboardAdmin')  

    context = {
        'book': book,
    }

    return render(request, 'InfoHaven_App/delete_book.html', context)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('DashboardAdmin')  
    else:
        form = BookForm() 

    return render(request, 'InfoHaven_App/add_book.html', {'form': form})

def profile(request):
    if 'member_id' in request.session:
        member_id = request.session['member_id']
        member_borrowed_books = BorrowingRecord.objects.filter(Member_ID=member_id, isReturned=0)

        # Calculate money penalty for each record
        for record in member_borrowed_books:
            record.calculate_money_penalty()

        context = {
            'borrowed_books': member_borrowed_books,
        }

        return render(request, 'InfoHaven_App/profile.html', context)

    return render(request, 'InfoHaven_App/profile.html')

def search_books(request):
    if request.method == 'GET':
        form = BookSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Perform the search in your database, e.g., using a filter query
            books = Book.objects.filter(title__icontains=search_query)
        else:
            books = []
    else:
        form = BookSearchForm()
        books = []

    return render(request, 'search_results.html', {'form': form, 'books': books})

def search_books_guest(request):
    if request.method == 'GET':
        form = BookSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Perform the search in your database, e.g., using a filter query
            books = Book.objects.filter(title__icontains=search_query)
        else:
            books = []
    else:
        form = BookSearchForm()
        books = []

    return render(request, 'search_results_guest.html', {'form': form, 'books': books})

def borrow_book(request, book_id):
    # Check if the user is logged in by checking if 'member_id' is in the session
    if 'member_id' not in request.session:
        return redirect('login')  # Redirect to the login page or any other appropriate action.

    member_id = request.session['member_id']
    
    try:
        member = Member.objects.get(Member_ID=member_id)
    except Member.DoesNotExist:
        return redirect('login')  # Redirect to the login page if the member doesn't exist.

    try:
        book = Book.objects.get(book_id=book_id, borrower=None)  # Get the book by its ID that is not already borrowed
    except Book.DoesNotExist:
        return redirect('InfoHaven_App/Dashboard.html')  # Redirect to the dashboard or any other appropriate action if the book is not available.

    book.borrower = member_id  # Associate the book with the member
    book.status = "Borrowed"  # Update the book's status
    book.save()  # Save the changes

    #For Naming convention of Record ID
    date_today = date.today()
    current_datetime = datetime.now()

    # Use the default string representation of the datetime object
    default_formatted_datetime = str(current_datetime)

    record_id = default_formatted_datetime + str(member_id) + str(book_id)
    dateToReturn = date_today + timedelta(days=7)
    
    borrowing_record = BorrowingRecord(
        Record_ID=record_id,
        book_id=book,
        Member_ID=member_id,
        date_borrowed=date_today,
        return_date=dateToReturn,
        isReturned=0,
        penalty=0
    )
    
    # Calculate initial money_penalty based on the number of days overdue
    borrowing_record.calculate_money_penalty()

    borrowing_record.save()

    return redirect('InfoHaven_App/profile.html')  # Redirect to the member's profile page

def update_member(request):
    if 'member_id' not in request.session:
        return redirect('login')  # Redirect if the member is not logged in

    member_id = request.session['member_id']
    member = Member.objects.get(Member_ID=member_id)

    if request.method == 'POST':
        form = UpdateMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            request.session['member_fname'] = form.cleaned_data['Fname']
            if member.Type == 0:
                return redirect('Start_Logged')
            else:
                return redirect('DashboardAdmin')  # Redirect to the member's home page after updating
    else:
        form = UpdateMemberForm(instance=member)

    return render(request, 'InfoHaven_App/update_member.html', {'form': form})

def delete_account(request):
    if 'member_id' in request.session:
        member_id = request.session['member_id']
        if request.method == 'POST':
            # Confirm the user's password to prevent accidental account deletion
            password = request.POST.get('password', '')
            try:
                member = Member.objects.get(Member_ID=member_id)
                if member.Password == password:
                    # Change the status of borrowed books to handle account deletion
                    borrowed_books = Book.objects.filter(borrower=member_id)
                    for book in borrowed_books:
                        book.status = "Available"  # You can set it to a different status as needed
                        book.borrower = None  # Remove the borrower
                        book.save()
                    
                    # Delete the account
                    member.delete()
                    
                    # Log out the user and redirect them to the homepage
                    request.session.clear()
                    return redirect('home')
                else:
                    messages.error(request, "Incorrect password. Please try again.")  # Add error message
            except Member.DoesNotExist:
                pass

    return render(request, 'InfoHaven_App/delete_account.html')

    return redirect('home')

def preview_book_guest(request, book_id):
    # Retrieve the book object from the database using the book_id
    book = get_object_or_404(Book, book_id=book_id)
    # Pass the book details to the template
    context = {
        'book_title': book.title,
        'book_author': book.author,
        'publication_date': book.date_published,
        'genre': book.classification,
        'isbn': book.isbn,
        'summary': book.summary,
        'availability': book.status,
    }
    return render(request, 'PreviewBookGuest.html', context)

def preview_book(request, book_id):
    # Retrieve the book object from the database using the book_id
    book = get_object_or_404(Book, book_id=book_id)

    # Pass the book details to the template
    context = {
        'book_title': book.title,
        'book_author': book.author,
        'publication_date': book.date_published,
        'genre': book.classification,
        'isbn': book.isbn,
        'summary': book.summary,
        'availability': book.status,
    }
    return render(request, 'PreviewBook.html', context)

def user_records(request):

    # Get all Borrowing records that are not returned
    records = BorrowingRecord.objects.filter(isReturned=0)

    for record in records:
            record.calculate_money_penalty()

    context = {
        'records' : records
    }

    return render(request, 'InfoHaven_App/user_records.html', context)

def return_book(request, record_id):
    if request.method == 'POST':
            
            # Get the book_id parameter from the POST data
            book_id = request.POST.get('book_id')
            date_returned = date.today()

            record = get_object_or_404(BorrowingRecord, Record_ID=record_id)
            book = get_object_or_404(Book, book_id=book_id)

            record.isReturned = 1
            record.date_returned = date_returned
            record.save()

            book.status = 'Available'
            book.borrower = None
            book.save()

    return redirect('UserRecords')

def pay_penalty(request, record_id):
    if request.method == 'POST':

        record = get_object_or_404(BorrowingRecord, Record_ID=record_id)
        record.return_date = date.today()
        record.penalty = 0.00
        record.save()

    return redirect('UserRecords') 



def penalties(request):
    if 'member_id' in request.session:
        member_id = request.session['member_id']
        member_borrowed_books = BorrowingRecord.objects.filter(Member_ID=member_id, isReturned=0)

        # Calculate money penalty for each record
        for record in member_borrowed_books:
            record.calculate_money_penalty()

        context = {
            'borrowed_books': member_borrowed_books,
        }

        return render(request, 'InfoHaven_App/penalties.html', context)

    return render(request, 'InfoHaven_App/penalties.html')


def extend_return_date(request, record_id):
    # Get the BorrowingRecord object
    record = get_object_or_404(BorrowingRecord, Record_ID=record_id)
   # Extend the return date by 3 days
    record.return_date += timedelta(days=3)
    record.isExtended = True  # Set a flag to indicate that it's extended
    record.save()  
       

    return redirect('penalties')  # Redirect back to the penalties page
