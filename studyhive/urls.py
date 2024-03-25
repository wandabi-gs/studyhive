from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from studyhive.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('interest/', include('interest.urls')),
    path('chat/', include('chat.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', Home, name='home')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
