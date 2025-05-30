from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
