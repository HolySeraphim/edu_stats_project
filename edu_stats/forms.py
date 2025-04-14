from django import forms
from .models import Student, Grade, Subject
from django.core.validators import EmailValidator

class StudentForm(forms.ModelForm):
    email = forms.CharField(
        validators=[EmailValidator(message="Введите корректный email адрес")],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@domain.com'
        })
    )

    class Meta:
        model = Student
        fields = ['name', 'group', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ФИО студента'
            }),
            'group': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер группы'
            }),
        }
        labels = {
            'name': 'ФИО',
            'group': 'Группа',
            'email': 'Email'
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'grade', 'date', 'comments']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите студента'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите предмет'
            }),
            'grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'step': '1'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительные комментарии'
            }),
        }
        labels = {
            'student': 'Студент',
            'subject': 'Предмет',
            'grade': 'Оценка',
            'date': 'Дата',
            'comments': 'Комментарии'
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }