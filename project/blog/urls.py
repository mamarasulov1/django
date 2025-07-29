from django.urls import path
# from .templates.blog import views
from .views import news_list
from django.conf import settings
from django.conf.urls.static import static

from .views import news_list,news_detail



urlpatterns = [
    path('' ,news_list, name="news-list"),
    path('<int:id>/', news_detail, name='news_detail')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
