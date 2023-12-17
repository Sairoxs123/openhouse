from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('teacher/', views.teacher, name="teacher"),
    path('teacher/add/', views.add, name="add"),
    path('teacher/add/student', views.addStudent, name="add-student"),
    path('teacher/delete/', views.delete, name="delete"),
    path('teacher/logout/', views.logout, name="logout"),
    path('student/', views.student, name="student")
]
