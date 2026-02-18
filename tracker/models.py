from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CATEGORY_CHOICES = [
    ("school", "School"),
    ("wellness", "Wellness"),
    ("work", "Work"),
    ("creativity", "Creativty"),
    ("home", "Home"),
]
class UserProfile(models.Model):
    
    DASHBOARD_CHOICES = [
        ("minimal", "Minimal"),
        ("colorful", "Colorful"),
        ("goal", "Goal-Focused"),
    ]

    FOCUS_CHOICES = [
        ("calm", "Calm visuals"),
        ("bright", "Bright colors"),
        ("minimal", "Minimal distractions"),
        ("gentle", "Gentle animations"),
    ]

    WORK_STYLE_CHOICES = [
        ("single", "One task at a time"),
        ("pomodoro", "Short bursts (Pomodoro-style)"),
        ("long", "Long focused sessions"),
        ("free", "No strict structure"),
    ]


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Nickname
    nickname = models.CharField(max_length=50)

    # Multi-select categories
    selected_categories = models.CharField(max_length=200, blank=False, default="")
    
    # Dashboard style (single choice)
    dashboard_style = models.CharField(
        max_length=50, 
        choices=DASHBOARD_CHOICES,
        default="minimal",
        blank=False
    )
    
    # Focus preference (single choice)
    focus_preference = models.CharField(
        max_length=50, 
        choices=FOCUS_CHOICES,
        default="calm",
        blank=False
    )
    
    # Work style (single choice)
    work_style = models.CharField(
        max_length=50, 
        choices=WORK_STYLE_CHOICES,
        default="one_task",
        blank=False
    )
    
    # Number of habits per day
    num_habits = models.PositiveIntegerField(default=3)
    
    # Optional: streak tracking
    streak = models.PositiveIntegerField(default=0)
    
    last_completed_day = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=50) # Name of the category (School, Wellness, etc.)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Link category to a user

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    class Meta:
        verbose_name_plural = "Categories"
    
class Habit(models.Model):
    name = models.CharField(max_length=100) # Name of the habit
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Link habit to a category
    user = models.ForeignKey(User, on_delete=models.CASCADE) # link habit to a user
    description = models.TextField(blank=True, null=True) # Optional description

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Task(models.Model):
    name = models.CharField(max_length=100) # Name of the task
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE) # Link task to a habit
    user = models.ForeignKey(User, on_delete=models.CASCADE) # link task to a user
    duration = models.PositiveIntegerField(null=True, blank=True) # Optional duration in minutes
    notes = models.TextField(blank=True, null=True) # Optional notes

    def __str__(self):
        return f"{self.name} ({self.habit.name})"

class TaskLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    duration = models.PositiveIntegerField(null=True, blank=True) # minutes
    date = models.DateField(default=timezone.now)

    def __str__(self):
        status = "Done" if self.completed else "Not done"
        return f"{self.user.username} - {self.task.habit.name}: {self.task.name} ({status})"