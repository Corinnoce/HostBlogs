from django.contrib import admin
from django.urls import path,include
from article.views import index
from django.conf.urls.static import static
from blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('articles/',include('article.urls'))
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
