from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import BorrowingRecord, Member, Book
from .forms import BookForm
from .forms import BookUpdateForm
from .forms import BookSearchForm
from .forms import UpdateMemberForm
from datetime import date, timedelta, datetime
from django.db.models import Q

# Create your views here.

def about(request):
    return render(request,"InfoHaven_App/about.html")

def about_guest(request):
    return render(request,"InfoHaven_App/about_guest.html")

def home(request):
    return render(request,"InfoHaven_App/introduction.html")

def forgot_password(request):
    return render(request, 'forgot_password.html')

def start(request):
    return render(request,"InfoHaven_App/start.html")

def start_logged(request):
    return render(request,"InfoHaven_App/start_logged.html")


# funtions
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
        member_requested_books = BorrowingRecord.objects.filter(Member_ID=member_id, isReturned=0, isRequested=1)
        member_borrowed_books = BorrowingRecord.objects.filter(Member_ID=member_id, isReturned=0, isRequested=0, isAccepted=1)
        member_old_borrowed_books = BorrowingRecord.objects.filter(Member_ID=member_id, isReturned=1)
        
        # Calculate money penalty for each record
        for record in member_borrowed_books:
            record.calculate_money_penalty()

        context = {
            'requested_books': member_requested_books,
            'borrowed_books': member_borrowed_books,
            'old_borrowed_books': member_old_borrowed_books
        }
        
        # Handle cancel request action
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'cancel':
                record_id = request.POST.get('record_id')
                record = get_object_or_404(BorrowingRecord, Record_ID=record_id)
                book = record.book_id
                record.isAccepted = 0
                record.isRequested = 0
                book.borrower = None
                book.status = "Available"
                book.save()
                record.delete()
                return redirect('profile')  # Redirect back to the profile after canceling request

        return render(request, 'InfoHaven_App/profile.html', context)
    
    return render(request, 'InfoHaven_App/profile.html')

def search_books(request):
    books = None
    form = BookSearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data['search_query']
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(isbn__icontains=query) |
            Q(publisher__icontains=query) |
            Q(date_published__icontains=query) |
            Q(status__icontains=query)|
            Q(classification__icontains=query)
        )

    return render(request, 'search_results.html', {'form': form, 'books': books})

def search_books_guest(request):
    books = None
    form = BookSearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data['search_query']
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(isbn__icontains=query) |
            Q(publisher__icontains=query) |
            Q(date_published__icontains=query) |
            Q(status__icontains=query)|
            Q(classification__icontains=query)
        )

    return render(request, 'search_results_guest.html', {'form': form, 'books': books})

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
        'status': book.status,
        'borrower': book.borrower,
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
        'status': book.status,
        'borrower': book.borrower,
    }
    return render(request, 'PreviewBook.html', context)

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
        member_borrowed_books = BorrowingRecord.objects.filter(Member_ID=member_id, isReturned=0, isAccepted=1)

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


######################################################

def borrow_request(request):
    if 'member_id' not in request.session:
        return redirect('login')  # Redirect to the login page or any other appropriate action

    member_id = request.session['member_id']

    try:
        member = Member.objects.get(Member_ID=member_id)
    except Member.DoesNotExist:
        return redirect('login')  # Redirect to the login page if the member doesn't exist

    # Get all Borrowing records that are not returned, not accepted, and are requested
    records = BorrowingRecord.objects.filter(isReturned=0, isAccepted=0, isRequested=1)

    for record in records:
        record.calculate_money_penalty()
        record.save()  # Save the penalty updates

    context = {
        'records': records
    }

    if request.method == 'POST':
        # Process the form submission
        record_id = request.POST.get('record_id')
        action = request.POST.get('action')

        if action == 'accept':
            # Handle accept action
            record = get_object_or_404(BorrowingRecord, Record_ID=record_id)
            book = record.book_id
            record.isAccepted = 1
            record.isRequested = 0
            # book.borrower = member.Member_ID  # Associate the book with the member's ID
            book.status = "Borrowed"  # Update the book's status
            book.save()  # Save the changes
            record.save()
            return redirect('user_records')  # Update to match your URL name
        elif action == 'decline':
            # Handle decline action
            record = get_object_or_404(BorrowingRecord, Record_ID=record_id)
            book = record.book_id  # Fetch the book associated with the record
            record.isAccepted = 0
            record.isRequested = 0
            book.borrower = None
            book.status = "Available"  # Update the book's status
            book.save()  # Save the changes
            record.delete()  # Delete the declined record
            return redirect('borrow_request')  # Update to match your URL name
        
    return render(request, 'borrow_request.html', context)

###################################################################################################

# def cancel_request(request):
#     if 'member_id' not in request.session:
#         return redirect('login')

#     member_id = request.session['member_id']

#     try:
#         member = Member.objects.get(Member_ID=member_id)
#     except Member.DoesNotExist:
#         return redirect('login')

#     records = BorrowingRecord.objects.filter(isReturned=0, isAccepted=0, isRequested=1)

#     for record in records:
#         record.calculate_money_penalty()
#         record.save()

#     context = {
#         'records': records
#     }

#     if request.method == 'POST':
#         record_id = request.POST.get('record_id')
#         action = request.POST.get('action')
        
#         if action == 'cancel':
#             record = get_object_or_404(BorrowingRecord, Record_ID=record_id)
#             book = record.book_id
#             record.isAccepted = 0
#             record.isRequested = 0
#             book.borrower = None
#             book.status = "Available"
#             book.save()
#             record.delete()
#             return redirect('profile')

#     return render(request, 'InfoHaven_App/profile.html', context)



###################################################################################################

def borrow_book(request, book_id):
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
        return redirect('dashboard')  # Redirect to the dashboard or any other appropriate action if the book is not available.

    # For Naming convention of Record ID
    date_today = date.today()
    current_datetime = datetime.now()
    default_formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
    record_id = f"{default_formatted_datetime}_{member_id}_{book_id}"
    dateToReturn = date_today + timedelta(days=7)
    
    borrowing_record = BorrowingRecord(
        Record_ID=record_id,
        book_id=book,
        Member_ID=member_id,
        date_borrowed=date_today,
        return_date=dateToReturn,
        isReturned=0,
        penalty=0.00,
        isAccepted=0,
        isRequested=1,
    )
    
    # Calculate initial money_penalty based on the number of days overdue
    borrowing_record.calculate_money_penalty()
    borrowing_record.save()
    
    # Update the book status to "Requested"
    book.status = "Requested"
    book.borrower = member.Member_ID  # Associate the book with the member's ID
    book.save()

    return redirect('profile')  # Redirect to the member's profile page

###################################################################################################

def user_records(request):
    # Fetch borrowing records where isAccepted is true and status is "Borrowed"
    records = BorrowingRecord.objects.filter(isAccepted=1, isRequested=0, isReturned=0, book_id__status="Borrowed").select_related('book_id')

    # Fetch the borrower's name for each record
    for record in records:
        member = get_object_or_404(Member, Member_ID=record.Member_ID)
        record.borrower_name = f"{member.Fname} {member.Lname}"  # Assuming you have first_name and last_name fields in the Member model

    context = {
        'records': records
    }
    return render(request, 'InfoHaven_App/user_records.html', context)

###################################################################################################


def notification(request):
    if 'member_id' in request.session:
        member_id = request.session['member_id']
        penalties = BorrowingRecord.objects.filter(Member_ID=member_id, isReturned=0, penalty__gt=0)
        
        context = {
            'penalties': penalties,
        }
        
        return render(request, "InfoHaven_App/notification.html", context)
    
    return redirect('Login')