from django.urls import path
#from .views import ArticleListView
from .views import ArticleListView, ArticleDetailView
from .views import (
    register_view, 
    my_site_view, 
    login_button, 
    logout_button, 
    finance_view, 
    ArticleCreateView, 
    CommentCreateView, 
    HoursListView,
    ScheduleListView,
)


app_name = 'articles'
urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('register/', register_view, name='register'),
    path('my_site/<int:user_id>/', my_site_view, name='my-site'),
    path('login_button/<int:user_id>/', login_button, name='login-button'),
    path('logout_button/<int:user_id>', logout_button, name='logout-button'),
    path('hours/<int:user_id>', HoursListView.as_view(), name='hours'),
    path('finance/<int:user_id>', finance_view, name='finance'),
    #path('schedule/<int:user_id>', schedule_view, name='schedule'),
    path('schedule/<int:user_id>', ScheduleListView.as_view(), name='schedule'),
    path('article_create/', ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/comment_create', CommentCreateView.as_view(), name='comment-create'),
    #path('comment/', comment_add_view, name='comment')
    #path('', ArticleListView.as_view(), name='article-list'),
]
