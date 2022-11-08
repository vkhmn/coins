from django.urls import path

from apps.coins.views import HomeView, filter_view, SettingsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('filter/', filter_view, name='filter'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
