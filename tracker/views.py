from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import UserProfile

from .forms import SurveyForm


# Home page view 
def index(request):
    return render(request, "tracker/index.html")

# Register page view 
def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # If passwords do not match  
        if password1 != password2:
            return render(request, "tracker/register.html", {
                "message": "Passwords do not match."
            })
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            return render(request, "tracker/register.html", {
                "message": "Username already exists."
            })
        
        # Create user
        user = User.objects.create_user(username=username, password=password1)
        user.save() 

        # Create an empty user profile
        UserProfile.objects.create(user=user)

        login(request, user)
        return redirect("survey")
            
    return render(request, "tracker/register.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    message = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            message = "Invalid username or password."

    return render(request, "tracker/login.html", {"message": message})


def logout_view(request):

    # Logout the currently logged-in user and clear out their session
    logout(request)

    # After logging out, send user back to the home page
    return redirect("index")


@login_required
def survey(request):
    try:
        profile = request.user.userprofile # Get the UserProfile if it exists
    except UserProfile.DoesNotExist:
        profile = None
    
    if request.method == "POST":
        form = SurveyForm(request.POST, instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect("dashboard") # Redirect to dashboard after submission
        
    else:
        form = SurveyForm(instance=profile)

    return render(request, "tracker/survey.html", {"form": form})
    

@login_required
def dashboard(request):
    # Get the user's profile, or redirect to survey if it does not exist
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect("survey")
    
    # Render the dashboard template and pass the profile (shows personalized info from survey)
    return render(request, "tracker/dashboard.html", {"profile": profile})


