from django.urls import path
from . import views
from .views import check_email_exists

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('ajax/check_email_exists/', check_email_exists, name='check_email_exists'),
]