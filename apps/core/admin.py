from django.contrib import admin
from apps.core.models import User, Filter, CoinUser


@admin.register(CoinUser)
class CoinUserAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    pass
