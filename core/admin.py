from django.contrib import admin
from core.models import *

# Register your models here.

@admin.register(Students)

class StudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade_sec', 'jssid')
    ordering = ('id',)
    search_fields = ('name', 'jssid')

@admin.register(Teachers)

class TeachersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject')
    ordering = ('id',)
    search_fields = ('name', 'subject')

@admin.register(Reservations)

class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'teacher', 'time')
    ordering = ('id',)
    search_fields = ('student', 'teacher', 'time')
