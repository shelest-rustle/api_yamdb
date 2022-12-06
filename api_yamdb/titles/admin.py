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

admin.site.register(Genre)

admin.site.register(Category)
