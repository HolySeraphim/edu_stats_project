from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    # Страницы добавления
    path('students/add/', views.add_student, name='add_student'),
    path('grades/add/', views.add_grade, name='add_grade'),

    # Страницы списков
    path('students/', views.StudentListView.as_view(), name='students_list'),
    path('grades/', views.GradeListView.as_view(), name='grades_list'),

    # Страницы предметов
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/', views.SubjectListView.as_view(), name='subjects_list'),

    # Аналитика
    path('statistics/', views.statistics_view, name='statistics'),

    # Страницы редактирования и удаления
    path('grades/<int:pk>/edit/', views.edit_grade, name='edit_grade'),
    path('grades/<int:pk>/delete/', views.delete_grade, name='delete_grade'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
]