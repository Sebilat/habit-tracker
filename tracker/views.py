from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from datetime import date, timedelta

from .models import UserProfile, TaskLog, Task, Habit

from .forms import SurveyForm

import json



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
    # Get the user's habits
    user_habits = Habit.objects.filter(user=request.user)
    
    # Get the user's profile, or redirect to survey if it does not exist
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # return redirect("survey")
        profile = None

    # Get today's date
    today = timezone.now().date()

    # ----Weekly Tracking Data (last 7 days)
    weekly_data = []

    for i in range(6, -1, -1): # 6 days ago -> today
        day = today - timedelta(days=i)
        logs = TaskLog.objects.filter(user=request.user, date=day)

        total_tasks = logs.count()
        completed_tasks = logs.filter(completed=True).count()

        # Tasks' Status
        if total_tasks == 0:
            status = "none" # no tasks at all

        elif completed_tasks == 0:
            status = "none" # tasks exist, none completed
        
        elif completed_tasks == total_tasks:
            status = "complete" # all tasks complete

        else:
            status = "partial" # some tasks complete

        weekly_data.append({
            "date": day,
            "day_label": day.strftime("%a"), # Mon, Tue, Wed
            "status": status,
            "total": total_tasks,
            "completed": completed_tasks,
        })


    # Get tasks for the logged-in user
    task_logs = TaskLog.objects.filter(user=request.user, date=today)

    # Handle adding a new task only
    if request.method == "POST":

        # Handle adding a new task
        task_name = request.POST.get("task_name")
        habit_id = request.POST.get("habit_id")

        # Only create a task if both fields are filled 
        if task_name and habit_id:
            habit = Habit.objects.get(id=habit_id)

            TaskLog.objects.create(
                user=request.user,
                date=today,

                # Logs the task for today, so it shows up on the dashboard
                task=Task.objects.create(
                    name=task_name,
                    habit=habit,
                    user=request.user
                ),
                completed=False
            ) 

        return redirect("dashboard") # Refresh page after update
    

    # Render the dashboard template and pass the profile (shows personalized info from survey)
    return render(request, "tracker/dashboard.html", {
        "profile": profile, 
        "task_logs": task_logs,
        "user_habits": user_habits,
        "weekly_data": weekly_data,
    })

@login_required
@require_POST
def toggle_task(request):
    data = json.loads(request.body)
    task_log_id = data.get("task_log_id")

    try:
        task_log = TaskLog.objects.get(id=task_log_id, user=request.user)
        task_log.completed = not task_log.completed
        task_log.save()

        return JsonResponse({
            "completed": task_log.completed
        })
    
    except TaskLog.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)
    
@login_required
def delete_task(request, task_id):
    """
    Deletes a Task (and its TaskLog) for the logged-in user.
    """

    try:
        # Get the Task object that belongs to this user
        task = Task.objects.get(id=task_id, user=request.user)

        # Delete all tasks logs associated with this task
        TaskLog.objects.filter(task=task, user=request.user).delete()

        # Delete the Task itself
        task.delete()

        # Redirect back to dashboard
        return redirect("dashboard")
    
    except Task.DoesNotExist:
        # If the task does not exist, just redirect
        return redirect("dashboard")

@login_required
@require_POST
def complete_day(request):
    """
    Mark the day as completed if all tasks are done.
    Increment the user's streak by 1.
    """

    today = timezone.now().date()
    task_logs = TaskLog.objects.filter(user=request.user, date=today)

    # Check if all tasks are completed
    if not task_logs.exists():
        return JsonResponse({
            "success": False,
            "message": "No tasks for today."
        })
    
    if not all(log.completed for log in task_logs):
        return JsonResponse({
            "success": False,
            "message": "Not all tasks are completed yet."
        })
    
    profile = request.user.userprofile

    # Prevent double streak increment same day
    if profile.last_completed_day == today:
        return JsonResponse({
            "success": False,
            "message": "You already completed today!"
        })
    
    # If yesterday was completed, streak continues
    if profile.last_completed_day == today - timedelta(days=1):
        profile.streak += 1

    else:
        profile.streak = 1 # restart streak

    profile.last_completed_day = today
    profile.save()

    return JsonResponse({
        "success": True,
        "streak": profile.streak
    })


