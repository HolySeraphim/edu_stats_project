from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Student(models.Model):
    """
    Модель для хранения информации о студентах
    """
    name = models.CharField(
        max_length=100,
        verbose_name='ФИО',
        help_text='Полное имя студента'
    )
    group = models.CharField(
        max_length=20,
        verbose_name='Группа',
        help_text='Учебная группа студента'
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        help_text='Электронная почта студента'
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['name']

    def __str__(self):
        return self.name

class Subject(models.Model):
    """
    Модель для хранения учебных дисциплин
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Название учебного предмета'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        help_text='Краткое описание предмета'
    )

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']

    def __str__(self):
        return self.name

class Grade(models.Model):
    """
    Модель для хранения оценок студентов
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Студент'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Предмет'
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка',
        help_text='Оценка от 1 до 5'
    )
    date = models.DateField(
        verbose_name='Дата оценки'
    )
    comments = models.TextField(
        verbose_name='Комментарии',
        blank=True,
        help_text='Дополнительные заметки'
    )

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ['-date', 'student']
        unique_together = ['student', 'subject', 'date']

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade} ({self.date})"

    def clean(self):
        if self.grade < 1 or self.grade > 5:
            raise ValidationError({'grade': 'Оценка должна быть от 1 до 5'})