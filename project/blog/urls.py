from django.urls import path
# from .templates.blog import views
from .views import news_list
from django.conf import settings
from django.conf.urls.static import static

from .views import news_list,news_detail,news_Cat,news_creat,tag_create,category_create,change_view,change_image,add_image,delete_img,delete_news
from .views import login_view,registr_view,logout_view

urlpatterns = [
    path('' ,news_list, name="news-list"),
    path('<int:id>/', news_detail, name='news_detail'),
    path('categories/<int:id>/',news_Cat, name='news_Cat'),
    path('creat/',news_creat, name='news_creat'),
    path('tag/create/', tag_create, name='tag_create'),
    path('category/create/', category_create, name='category_create'),
    path('change/<int:id>/', change_view, name='change'),
    path('image/change/<int:id>/', change_image, name='change_image'),
    path('image/add/<int:id>/', add_image, name='add_image'),
    path('delete/img/<int:id>/', delete_img, name='delete_img'),
    path('delete/news/<int:id>/', delete_news, name='delete_news'),
    path('login', login_view, name='login_'),
    path('register', registr_view, name='register_'),
    path('logout', logout_view,name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    