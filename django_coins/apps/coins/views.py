from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import ListView,UpdateView

from apps.coins.forms import PatternFormSet
from apps.coins.models import Coin
from apps.core.models import CoinUser, User


class HomeView(LoginRequiredMixin, ListView):
    model = Coin
    template_name = 'core/index.html'
    context_object_name = 'coins'
    login_url = reverse_lazy('login')
    paginate_by = 10

    def get_queryset(self):
        return CoinUser.objects.select_related(
            'coin'
        ).filter(
            user=self.request.user
        ).filter(
            coin__time_end__gte=datetime.now()
        ).order_by('-coin__time_create')


class ArchiveView(HomeView):
    def get_queryset(self):
        return CoinUser.objects.select_related(
            'coin'
        ).filter(
            user=self.request.user
        ).filter(
            coin__time_end__lt=datetime.now()
        ).order_by('-coin__time_create')


@login_required
def filter_view(request):
    formset = PatternFormSet(instance=request.user)
    if request.method == 'POST':
        formset = PatternFormSet(request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
            return redirect('/filter/')

    context = {'patterns': formset}
    return render(request, 'core/filter.html', context)


class SettingsView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = '/settings/'
    context_object_name = 'user'
    template_name = 'core/settings.html'
    fields = ['chat_id', 'unc_pattern']

    def get_object(self, queryset=None):
        return self.request.user

