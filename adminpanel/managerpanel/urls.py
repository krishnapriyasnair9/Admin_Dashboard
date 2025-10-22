from django.urls import path
from .views import (
    AdminLoginView,
    DashboardView, BannerUpdateView, admin_logout
)
urlpatterns = [
    path('', AdminLoginView.as_view(), name='login'),
    path('logout/', admin_logout, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('update-banner/', BannerUpdateView.as_view(), name='update_banner'),
    ]