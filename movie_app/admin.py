from django.contrib import admin, messages
from .models import Movie, Director, Actor, DressingRoom
from django.db.models import QuerySet


# Register your models here.

@admin.register(DressingRoom)
class DressingRoomAdmin(admin.ModelAdmin):
    list_display = ['floor', 'number', 'actor']



@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_display = ['first_name', 'last_name', 'gender']
    list_editable = ['gender']
    search_fields = ['first_name','last_name', 'gender']
    list_filter = ['first_name', 'last_name', 'gender']

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_display = ['first_name', 'last_name', 'email']
    list_editable = ['email']
    search_fields = ['first_name','last_name', 'email']
    list_filter = ['first_name', 'last_name']


class RatingFilter(admin.SimpleListFilter):
    title = 'Фильтр по рейтингу'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('< 40', 'Низкий'),
            ('от 40 до 59', 'Средний'),
            ('от 60 до 79', 'Высокий'),
            ('>= 80', 'Топ'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '< 40':
            return queryset.filter(rating__lt=40)
        elif self.value() == 'от 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        elif self.value() == 'от 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        elif self.value() == '>= 80':
            return queryset.filter(rating__gte=80)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # для отображения в админке
    # fields = ['name', 'rating']  # для отображения редактируемых полей
    # exclude = ['slug']  # исключает отображение определённых полей (обратное fields)
    # readonly_fields = ['budget']  # запрещает редактировать определённые поля, но они отображаются
    prepopulated_fields = {'slug': ('name',)}  # для вычисляемых полей
    list_display = ['name', 'rating', 'year', 'currency', 'budget', 'rating_status', 'director']
    list_editable = ['rating', 'year', 'currency', 'budget', 'director']
    ordering = ['-rating']  # для отсортированного отображения
    list_per_page = 10
    actions = ['set_dollars', 'set_euro']
    search_fields = ['name__startswith', 'rating']  # для добавления поисковой строки в админку и поиска по определённым полям
    list_filter = ['name', 'currency', RatingFilter]
    filter_horizontal = ['actors']

    @admin.display(ordering='rating', description='Статус')  # для сортировки как по рейтингу
    def rating_status(self, mov:Movie):
        if mov.rating < 50:
            return 'Зачем это смотреть?!'
        elif mov.rating < 70:
            return 'Разок можно глянуть'
        elif mov.rating <= 85:
            return 'Зачёт'
        return 'Топчик'

    @admin.action(description='Установить валюту в доллары')
    def set_dollars(self, request, queryset: QuerySet):
        queryset.update(currency=Movie.USD)

    @admin.action(description='Установить валюту в евро')
    def set_euro(self, request, queryset: QuerySet):
        count_updated = queryset.update(currency=Movie.EURO)
        self.message_user(request,
                          f'Было обновлено {count_updated} записей',
                          messages.ERROR  # изменяет уровень сообщений (как ошибку делает красным)
        )

# admin.site.register(Movie, MovieAdmin)  # вместо декоратора можно использовать
