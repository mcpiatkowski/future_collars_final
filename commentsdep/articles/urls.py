from django.urls import path
#from .views import ArticleListView
from .views import article_view, article_detail
from .views import register_view, login_view, logout_user_view, my_site_view, login_button, logout_button


app_name = 'articles'
urlpatterns = [
    path('', article_view, name='home'),
    path('<int:article_id>/', article_detail, name='article-detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('my_site/<int:user_id>/', my_site_view, name='my-site'),
    path('login_button/<int:user_id>/', login_button, name='login_button'),
    path('logout_button/<int:user_id>', logout_button, name='logout_button'),
    #path('comment/', comment_add_view, name='comment')
    #path('', ArticleListView.as_view(), name='article-list'),
]
