from django.apps import apps
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from .models import Article, HoursWorked, Profile, Blacklist, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CommentForm, CommentCreateForm, CreateUserForm, ArticleCreateForm
from datetime import datetime, date
from .filters import ArticleFilter
import decimal
from math import floor
from django.http import HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin


### LOGIN AND REGISTRATION ############

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/articles')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                user = User.objects.filter(email=email).first()
                user.is_active = False
                user.save()
                Profile.objects.create(user=user)
            return redirect('/articles/login')
        context = {
            'form': form,
        }
        return render(request, 'articles/register.html', context)


class ArticleListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        queryset = apps.get_model('articles.Article').objects.all()
        myFilter = ArticleFilter(self.request.GET, queryset=queryset)
        return myFilter.qs


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'articles/article_create.html'
    form_class = ArticleCreateForm
    queryset = Article.objects.all()
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = apps.get_model('articles.Article')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentCreateForm()
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk']
        form.instance.user = self.request.user
        comment = form.cleaned_data.get('content').split(' ')
        if Blacklist.objects.validate_words(comment):
            messages.warning(self.request, 
                f'Komentarz przekazany do moderacji.'
                )
            messages.error(self.request, 
                f'Proszę się wyrażać!'
                )
            return HttpResponseRedirect(reverse(
                'articles:article-detail', 
                kwargs={'pk': self.kwargs['pk']}
                ))
        messages.success(self.request, 
                f'Dodano post.'
                ) 
        return super().form_valid(form)


class HoursListView(LoginRequiredMixin, ListView):
    template_name = 'articles/hours.html'

    def get_queryset(self):
        return User.objects.get(pk=self.kwargs['user_id'])


class ScheduleListView(LoginRequiredMixin, ListView):
    template_name = 'articles/schedule.html'

    def get_queryset(self):
        return User.objects.get(pk=self.kwargs['user_id'])


@login_required(login_url='/articles/login')
def my_site_view(request, user_id):
    user = User.objects.get(pk=user_id)
    context ={
        'user': user,
        'login_status': user.profile.logged,
    }
    return render(request, 'articles/my_site.html', context)


@login_required(login_url='/articles/login')
def finance_view(request, user_id):
    user = User.objects.get(pk=user_id)
    current_month = timezone.now().month
    month = user.hoursworked_set.filter(day__month = current_month)
    current_month = datetime.now().strftime('%B').lower()
    payment = 0.0
    for day in month:
        if day.salary:
            payment += day.salary
    context ={
        'user': user,
        'payment': floor(payment*100)/100,
        'month': current_month,
    }
    return render(request, 'articles/finance.html', context)


@login_required(login_url='/articles/login')
def login_button(request, user_id):
    if request.user.is_authenticated:
        ip = request.META.get('REMOTE_ADDR')
        print("MOJE IP: ", ip)
        user = User.objects.get(pk=user_id)
        user.profile.logged = True
        user.profile.save()
        login_status = user.profile.logged
        user.hoursworked_set.create(
            start=timezone.now(),
            )
    return redirect("articles:my-site", user_id=user_id)


@login_required(login_url='/articles/login')
def logout_button(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=user_id)
        if user.profile.logged:
            user.profile.logged = False
            user.profile.save()
            hours = user.hoursworked_set.latest('start')
            hours.finish = timezone.now()
            salary = apps.get_model('articles.HoursWorked').objects.total_salary(hours)
            #Payslip.objects.update(hours)
            hours.save()
    return redirect("articles:my-site", user_id=user_id)