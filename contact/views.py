from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Users
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from .models import Users, SpamReport
from django.contrib.auth.models import User

@login_required
def index(request):
    # Render Homepage on successful login
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Save the user form data
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            # Create the Users model entry
            users_data = Users(
                user=user,
                name=request.POST.get('username'),
                phone_number=request.POST.get('phone'),
                email=request.POST.get('email', ''),
            )
            users_data.save()  

            login(request, user)

            messages.success(request, "Registration successful!")
            print("Registration successful!")
            # Redirect to login page after successful registration
            return redirect('index') 
        else:
            messages.error(request, "There was an error with your registration form.")
            print("There was an error with your registration form.")
    else:
        user_form = UserRegistrationForm()

    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the homepage after successful login
            return redirect('index')  
        else:
            # Check if the username exists
            from django.contrib.auth.models import User
            if not User.objects.filter(username=username).exists():
                messages.error(request, "User does not exist. Please register.")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    # Logout for authenticated user
    logout(request)
    return redirect('login')

@login_required
def search(request):
    context = {}

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')  # Retrieve the phone number from the form input

        if phone_number:
            # Check if the phone number exists in the SpamReport table
            spam_info = SpamReport.objects.filter(phone_number=phone_number).first()

            # Retrieve the name associated with the phone number in the Users table
            user = Users.objects.filter(phone_number=phone_number).first()
            if user:
                associated_name = user.name
            else:
                associated_name = None

            # Information about the phone number
            context['phone_number'] = phone_number
            context['is_spam'] = spam_info is not None 
            context['spam_count'] = spam_info.spam_count if spam_info else 0 
            context['associated_name'] = associated_name
        else:
            # If no phone number is provided add error to the context
            context['error'] = "Please enter a valid phone number."

    return render(request, 'search.html', context)

@login_required
def report_spam(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        if phone_number:
            # Check if the SpamReport already exists for the number
            spam_report, created = SpamReport.objects.get_or_create(phone_number=phone_number)

            # Check if the current user has already reported this number
            if request.user in spam_report.reported_by.all():
                return render(request, 'report_spam.html', {
                    'error': f"You have already reported the number {phone_number}."
                })

            # Add the user to the reported_by list and increment spam_count
            spam_report.reported_by.add(request.user)
            spam_report.spam_count += 1
            spam_report.save()

            return render(request, 'report_spam.html', {
                'success': f"Successfully reported the number {phone_number} as spam."
            })

    return render(request, 'report_spam.html')
