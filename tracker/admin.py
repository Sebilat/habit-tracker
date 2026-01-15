from django.contrib import admin
from .models import UserProfile, Category, Habit, Task, TaskLog

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Habit)
admin.site.register(Task)
admin.site.register(TaskLog)
