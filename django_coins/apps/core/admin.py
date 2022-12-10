from django.contrib import admin
from apps.core.models import User, Filter, CoinUser
from django.contrib.auth.admin import UserAdmin

from apps.core.forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CoinUser)
class CoinUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    pass


class CoinUserInline(admin.TabularInline):
    model = CoinUser


class FilterInline(admin.TabularInline):
    model = Filter


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Telegram', {'fields': ('chat_id', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    inlines = [
        FilterInline,
        CoinUserInline
    ]

