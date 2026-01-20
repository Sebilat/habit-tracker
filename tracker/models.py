from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    selected_categories = models.TextField()
    dashboard_style = models.CharField(max_length=50)
    focus_preference = models.CharField(max_length=50)
    work_style = models.CharField(max_length=50)
    num_habits = models.PositiveIntegerField(default=3)
    streak = models.PositiveIntegerField(default=0)

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
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        status = "Done" if self.completed else "Not done"
        return f"{self.user.username} - {self.task.habit.name}: {self.task.name} ({status})"