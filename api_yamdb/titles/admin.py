from django.contrib import admin

from .models import Title, Genre, Category

from users.models import User

admin.site.register(User)


class TitleAdmin(admin.ModelAdmin):
    """
    Административная модель произведения.
    """
    list_display = ('name', 'year', 'description', 'genre', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    list_editable = ('category',)


admin.site.register(Title, TitleAdmin)


class GenreAdmin(admin.ModelAdmin):
    """
    Административная модель жанра.
    """
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Genre, GenreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    """
    Административная модель категории.
    """
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
