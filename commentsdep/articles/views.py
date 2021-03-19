from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from .models import Article, HoursWorked, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CommentForm, CreateUserForm
from datetime import datetime, date

""" class ArticleListView(ListView):
    template_name = 'articles/article_list.html'
    queryset = Article.objects.all()
 """

@login_required(login_url='/articles/login')
def article_view(request):
    queryset = Article.objects.all()
    context ={
        'object_list': queryset,
    }
    return render(request, 'articles/article_list.html', context)


@login_required(login_url='/articles/login')
def article_detail(request, article_id):
    blacklist = [
        'kurczaki',
        'motyla noga',
        'kurtka na wacie',
        'wirus',
    ]

    article = Article.objects.get(pk=article_id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            for word in form.cleaned_data['comment'].split(' '):
                if word in blacklist:
                    return redirect('articles:article-detail', article_id=article_id)
            article.comment_set.create(user=request.user, content=form.cleaned_data['comment'])
            form = CommentForm()
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/article_detail.html', context)


@login_required(login_url='/articles/login')
def my_site_view(request, user_id):
    user = User.objects.get(pk=user_id)
    context ={
        'user': user,
        'login_status': user.profile.logged,
    }
    return render(request, 'articles/my_site.html', context)


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
    context ={
        'user': user,
        'login_status': login_status,
    }
    return render(request, 'articles/my_site.html', context)
#    return redirect("articles:my-site", user_id=user_id)


@login_required(login_url='/articles/login')
def logout_button(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=user_id)
        if user.profile.logged:
            user.profile.logged = False
            user.profile.save()
            hours = user.hoursworked_set.latest('start')
            hours.finish = timezone.now()
            hours.save()
    return redirect("articles:my-site", user_id=user_id)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/articles')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                print("TU JESTEM")
                form.save()
                email = form.cleaned_data['email']
                user = User.objects.filter(email=email).first()
                user.is_active = False
                user.save()
                Profile.objects.create(user=user)
                print("BANG!")
            return redirect('/articles/login')
        context = {
            'form': form,
        }
        return render(request, 'articles/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/articles')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/articles')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'articles/login.html', context)


def logout_user_view(request):
    logout(request)
    return redirect('/articles/login')
