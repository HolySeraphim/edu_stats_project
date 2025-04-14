from django.test import TestCase
from django.urls import reverse
from .models import Student, Subject, Grade
from django.utils import timezone

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Иванов Иван",
            group="Группа 101",
            email="ivanov@example.com"
        )

    def test_student_creation(self):
        self.assertEqual(self.student.name, "Иванов Иван")
        self.assertEqual(self.student.group, "Группа 101")

class GradeViewTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Тестовый Студент",
            group="Группа 101",
            email="test@example.com"
        )
        self.subject = Subject.objects.create(
            name="Математика",
            description="Тестовая дисциплина"
        )

    def test_add_grade_view(self):
        response = self.client.get(reverse('add_grade'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grades/add_grade.html')

    def test_grade_creation(self):
        grade = Grade.objects.create(
            student=self.student,
            subject=self.subject,
            grade=5,
            date=timezone.now()
        )
        self.assertEqual(grade.grade, 5)