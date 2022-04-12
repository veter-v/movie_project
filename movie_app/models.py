from django.db import models
from django.urls import reverse
from django.utils.text import slugify  # выполняет преобразование текста в slug формат
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
# Создание таблицы при помощи ORM

class DressingRoom(models.Model):
    floor = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return f'{self.floor} {self.number}'


class Actor(models.Model):

    FEMALE = 'F'
    MALE = 'M'
    GENDER_CHOICES = [
        (FEMALE, 'Женщина'),
        (MALE, 'Мужчина'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    slug = models.SlugField(default='', null=False, db_index=True)
    dressing = models.OneToOneField(DressingRoom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.gender == self.MALE:
            return f'Актёр {self.first_name} {self.last_name}'
        else:
            return f'Актриса {self.first_name} {self.last_name}'

    def get_url(self):
        return reverse('actor-detail', args=[self.slug])


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    slug = models.SlugField(default='', null=False, db_index=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # def save(self, *args, **kwargs):
    #     temp = f'{self.first_name} {self.last_name}'
    #     self.slug = slugify(temp)
    #     super(Director, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('director-detail', args=[self.slug])


class Movie(models.Model):

    EURO = 'EUR'  # правильнее ссылаться на константы
    USD = "USD"
    RUB = 'RUB'
    CURRENCY_CHOICES = [
        (EURO, 'Euro'),
        (USD, 'Dollar'),
        (RUB, 'Rubles')
    ]

    name = models.CharField(max_length=40)  # name varchar(40)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    year = models.IntegerField(null=True, blank=True)  # blank для пустых значений в админке
    budget = models.IntegerField(default=1_000_000, blank=True, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=RUB)  # поле с выбором ответа
    slug = models.SlugField(default='', null=False, db_index=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    def get_url(self):
        # для автоматической генерации ссылки
        return reverse('movie-detail', args=[self.slug])

    def __str__(self):
        # переопределим отображение класc
        return f'{self.name} - {self.rating}%'

# from movie_app.models import Movie
# from django.db.models import Q
