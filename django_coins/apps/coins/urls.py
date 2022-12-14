from django.urls import path

from apps.coins.views import HomeView, filter_view, SettingsView, ArchiveView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('filter/', filter_view, name='filter'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
