from django.apps import apps
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import Article, HoursWorked, Profile, Blacklist, Comment, Payslip
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CommentForm, CommentCreateForm, CreateUserForm, ProfileForm, ArticleCreateForm, UserUpdateForm
from datetime import datetime, date
from .filters import ArticleFilter
import decimal
from math import floor
from django.http import HttpResponseRedirect, JsonResponse
from django.template.defaultfilters import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

### LOGIN AND REGISTRATION ############

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
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
            return redirect('/accounts/login')
        context = {
            'form': form,
        }
        return render(request, 'registration/register.html', context)


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
    template_name = 'articles/article_detail.html'
    model = Comment
    form_class = CommentCreateForm

    def get_success_url(self):
        return reverse('articles:article-detail', args=[self.kwargs['article_id']])

    def form_invalid(self, form):
        messages.add_message(self.request,messages.WARNING,"Komentarz nie może być pusty!")
        return redirect(reverse(
                'articles:article-detail', 
                args=[self.kwargs['article_id']]
                ))
    
    def form_valid(self, form):
        form.instance.article_id = self.kwargs['article_id']
        form.instance.user = self.request.user
        comment = form.cleaned_data.get('content').split(' ')
        if Blacklist.objects.validate_words(comment):
            messages.warning(self.request, f'Komentarz wysłany do moderacji')
            messages.error(self.request, f'Proszę się wyrażać!')
            return HttpResponseRedirect(reverse('articles:article-detail', 
                kwargs={'pk': self.kwargs['article_id']}
                ))
            messages.success(self.request, f'Dodano post.') 
        return super().form_valid(form)


class HoursListView(LoginRequiredMixin, ListView):
    template_name = 'articles/hours.html'
    paginate_by = 10
    model = HoursWorked

    def get_queryset(self):
        return HoursWorked.objects.filter(user=self.request.user)


""" 
    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def has_permission(self):
        return self.get_queryset() == self.request.user 

 """

class ScheduleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'articles/schedule.html'
    
    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id)

    def has_permission(self):
        return self.get_queryset() == self.request.user 


class MySiteView(LoginRequiredMixin, UpdateView):
    template_name = 'articles/my_site.html'
    model = Profile
    fields = ['image']

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.id)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_status'] = self.request.user.profile.logged
        context['user'] = self.request.user
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['profile_form'] = ProfileForm(instance=self.request.user.profile)
        return context


    def form_valid(self, form):
        submit_type = self.request.POST.get('submit_type')
        if submit_type == 'image':
            form = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
            return super().form_valid(form)


class FinanceView(LoginRequiredMixin, ListView):
    template_name = 'articles/finance.html'
    model = Payslip


""" 
@login_required(login_url='/accounts/login')
def finance_view(request):
    user = request.user
    if user.payslip_set:
        payslip = apps.get_model('articles.Payslip').objects.filter(user=user).last()
        month = payslip.month
        month = date(month, 'F')
        now = timezone.now()
        print("NOW: ", now)
    context ={
        'user': user,
        'payslip': payslip,
        'month': month,
    }
    return render(request, 'articles/finance.html', context)
 """

@login_required(login_url='/accounts/login')
def login_button(request):
    if request.user.is_authenticated:
        ip = request.META.get('REMOTE_ADDR')
        print("MOJE IP: ", ip)
        user = request.user
        user.profile.logged = True
        user.profile.save()
        login_status = user.profile.logged
        user.hoursworked_set.create(
            start=timezone.now(),
            )
    return redirect("articles:my-site")


@login_required(login_url='/accounts/login')
def logout_button(request):
    if request.user.is_authenticated:
        user = request.user
        if user.profile.logged:
            user.profile.logged = False
            user.profile.save()
            hours = user.hoursworked_set.latest('start')
            hours.finish = timezone.now()
            salary = apps.get_model('articles.HoursWorked').objects.total_salary(hours)
            apps.get_model('articles.Payslip').objects.update(hours)
            hours.save()
    return redirect("articles:my-site")


##### AJAX VIEWS ##########

def get_time(request):
#    time, salary = request.user.profile.get_last_pending_hours_worked()
    time, salary = request.user.profile.get_last_pending_hours_worked()
    #salary = request.user.profile.get_last_pending_hours_worked()[1]
    data = {
        'salary': salary,
        'time': time,
    }
    return JsonResponse(data)