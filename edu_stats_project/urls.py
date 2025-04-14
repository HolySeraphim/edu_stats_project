from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from edu_stats.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('', include('edu_stats.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "EduStats - Администрирование"
admin.site.site_title = "Панель управления EduStats"
admin.site.index_title = "Добро пожаловать в систему образовательной статистики"