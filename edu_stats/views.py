from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Avg, Count
from .models import Grade, Student, Subject
from .forms import StudentForm, GradeForm, SubjectForm
from collections import defaultdict


def home_view(request):
    return render(request, 'grades/home.html')


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades:students_list')
    else:
        form = StudentForm()

    context = {
        'form': form,
        'title': 'Добавление студента'
    }
    return render(request, 'grades/add_student.html', context)


def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades:grades_list')  # Используем пространство имен
    else:
        form = GradeForm()

    context = {
        'form': form,
        'title': 'Добавление оценки'
    }
    return render(request, 'grades/add_grade.html', context)


class StudentListView(ListView):
    model = Student
    template_name = 'grades/students_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список студентов'
        return context

    def get_queryset(self):
        return Student.objects.all().order_by('name')

class GradeListView(ListView):
    model = Grade
    template_name = 'grades/grades_list.html'
    context_object_name = 'grades'
    paginate_by = 15
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список оценок'
        return context


def statistics_view(request):
    context = {'title': 'Статистика успеваемости'}

    subjects_with_grades = Subject.objects.filter(grades__isnull=False).distinct()
    if subjects_with_grades.exists():
        context['subjects_stats'] = subjects_with_grades.annotate(
            avg_grade=Avg('grades__grade'),
            grade_count=Count('grades')
        ).order_by('-avg_grade')

    if Grade.objects.exists():
        context['group_stats'] = Grade.objects.values(
            'student__group'
        ).annotate(
            avg_grade=Avg('grade'),
            grade_count=Count('id')
        ).order_by('-avg_grade')

    top_students = Student.objects.annotate(
        grade_count=Count('grades'),
        avg_grade=Avg('grades__grade')
    ).filter(grade_count__gte=3).order_by('-avg_grade')[:5]

    if top_students:
        context['top_students'] = top_students

    return render(request, 'grades/statistics.html', context)

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades:subjects_list')
    else:
        form = SubjectForm()
    return render(request, 'grades/add_subject.html', {'form': form})

def edit_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grades:grades_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'grades/edit_grade.html', {'form': form})

def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grades:grades_list')
    return render(request, 'grades/confirm_delete.html', {'grade': grade})


def delete_student(request, pk):  # Обратите внимание на параметр pk
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('grades:students_list')
    return render(request, 'grades/confirm_delete_student.html', {'student': student})


class SubjectListView(ListView):
    model = Subject
    template_name = 'grades/subjects_list.html'
    context_object_name = 'subjects'


def grades_table_view(request):
    # Получаем параметры фильтрации
    subject_id = request.GET.get('subject')  # Новый параметр для предмета
    student_id = request.GET.get('student')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Базовый запрос с фильтрацией
    grades = Grade.objects.all()

    if subject_id:  # Фильтр по предмету
        grades = grades.filter(subject_id=subject_id)
    if student_id:
        grades = grades.filter(student_id=student_id)
    if date_from:
        grades = grades.filter(date__gte=date_from)
    if date_to:
        grades = grades.filter(date__lte=date_to)

    # Получаем уникальные даты для столбцов
    dates = grades.dates('date', 'day').order_by('date')

    # Группируем оценки и вычисляем средние
    student_grades = defaultdict(dict)
    student_averages = {}  # Новый словарь для средних значений

    for grade in grades:
        student_grades[grade.student][grade.date] = grade.grade

    # Вычисляем средний балл для каждого студента
    for student in student_grades:
        grades_list = list(student_grades[student].values())
        student_averages = {
            student: grades.filter(student=student).aggregate(Avg('grade'))['grade__avg']
            for student in Student.objects.filter(grades__in=grades).distinct()
        }

    # Сортируем студентов по имени
    sorted_students = sorted(
        student_grades.keys(),
        key=lambda s: student_averages.get(s, 0),
        reverse=True
    )

    context = {
        'title': 'Таблица оценок',
        'dates': dates,
        'student_grades': dict(student_grades),
        'sorted_students': sorted_students,
        'student_list': Student.objects.all().order_by('name'),
        'subject_list': Subject.objects.all().order_by('name'),  # Список предметов для фильтра
        'selected_subject_id': int(subject_id) if subject_id else None,  # Для сохранения выбора
        'request': request,
        'student_averages': student_averages,
    }
    return render(request, 'grades/grades_table.html', context)