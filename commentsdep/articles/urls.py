from django.urls import path
#from .views import ArticleListView
from .views import ArticleListView, ArticleDetailView
from .views import (
    register_view, 
    #my_site_view, 
    login_button,
    logout_button,
    finance_view,
    ArticleCreateView, 
    CommentCreateView,
    HoursListView,
    ScheduleListView,
    MySiteView,
    get_time
)


app_name = 'articles'
urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('register/', register_view, name='register'),
    #path('my_site/', my_site_view, name='my-site'),
    path('my_site/', MySiteView.as_view(), name='my-site'),
    path('login_button/', login_button, name='login-button'),
    path('logout_button/', logout_button, name='logout-button'),
    path('hours/', HoursListView.as_view(), name='hours'),
    path('finance/', finance_view, name='finance'),
    #path('schedule/<int:user_id>', schedule_view, name='schedule'),
    path('schedule/', ScheduleListView.as_view(), name='schedule'),
    path('article_create/', ArticleCreateView.as_view(), name='article-create'),
    path('article/comment_create/<int:article_id>/', CommentCreateView.as_view(), name='comment-create'),
    path('get_time/', get_time, name='get-time')
    #path('comment/', comment_add_view, name='comment')
    #path('', ArticleListView.as_view(), name='article-list'),
]
