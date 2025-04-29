from django.contrib import admin
from .models import User, Resume, Vacancy, Application, News, Review, ContactRequest
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name', 'patronymic', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('patronymic', 'phone', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('patronymic', 'phone', 'role')}),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name', 'patronymic')
    ordering = ('email',)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    search_fields = ('title', 'user__email')
    list_filter = ('created_at',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'employment_type', 'published_at')
    search_fields = ('title', 'location')
    list_filter = ('employment_type', 'published_at')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'vacancy', 'status', 'applied_at')
    search_fields = ('user__email', 'vacancy__title')
    list_filter = ('status', 'applied_at')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'author')
    search_fields = ('title', 'author__email')
    list_filter = ('published_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'is_published')
    search_fields = ('user__email',)
    list_filter = ('is_published', 'created_at')


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'status')
    search_fields = ('name', 'email')
    list_filter = ('status', 'submitted_at')
