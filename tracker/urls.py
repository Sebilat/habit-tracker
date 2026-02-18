from django.urls import path
from .import views

urlpatterns = [
    path("", views.index, name='index'),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("survey/", views.survey, name="survey"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("toggle-task/", views.toggle_task, name="toggle_task"),
    path("delete-task/<int:task_id>/", views.delete_task, name="delete_task"),
    path("complete-day/", views.complete_day, name="complete_day"),
    path("select-goal-category/", views.select_goal_category, name="select_goal_category"),

    path("set-goal-category/<str:category>/", views.set_goal_category, name="set_goal_category"),
]