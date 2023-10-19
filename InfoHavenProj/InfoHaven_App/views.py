from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Member; 
from .models import Book
from .forms import BookForm
from .forms import BookUpdateForm


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

# Place views that has no code below.

def start(request):
    return render(request,"InfoHaven_App/start.html")

def start_logged(request):
    return render(request,"InfoHaven_App/start_logged.html")
   
#Book Views

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
    return render(request, 'InfoHaven_App/profile.html', {'request': request})

def borrow_book(request, book_id):
    # Check if the user is logged in and is a member
    if not request.user.is_authenticated or not request.user.member:
        return redirect('login')  # Redirect to the login page or any other appropriate action.

    member = request.user.member  # Get the member associated with the logged-in user
    try:
        book = Book.objects.get(book_id=book_id, borrower=None)  # Get the book by its ID that is not already borrowed
    except Book.DoesNotExist:
        return redirect('dashboard')  # Redirect to the dashboard or any other appropriate action if the book is not available.

    book.borrower = member  # Associate the book with the member
    book.status = "Borrowed"  # Update the book's status
    book.save()  # Save the changes

    return redirect('profile')  # Redirect to the member's profile page