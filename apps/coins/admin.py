from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from apps.coins.models import Coin, Seller, Category


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
#    prepopulated_fields = {"id": ("title",)}
    pass


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    #    prepopulated_fields = {"id": ("title",)}
    pass
