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

    def __str__(self):
        return self.user.username


