# Generated by Django 4.2 on 2025-04-14 13:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Полное имя студента', max_length=100, verbose_name='ФИО')),
                ('group', models.CharField(help_text='Учебная группа студента', max_length=20, verbose_name='Группа')),
                ('email', models.EmailField(help_text='Электронная почта студента', max_length=254, unique=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название учебного предмета', max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, help_text='Краткое описание предмета', verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(help_text='Оценка от 1 до 5', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('date', models.DateField(verbose_name='Дата оценки')),
                ('comments', models.TextField(blank=True, help_text='Дополнительные заметки', verbose_name='Комментарии')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='edu_stats.student', verbose_name='Студент')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='edu_stats.subject', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
                'ordering': ['-date', 'student'],
                'unique_together': {('student', 'subject', 'date')},
            },
        ),
    ]
