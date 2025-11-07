from django.urls import path
from .views import (
    AdminLoginView, DashboardView, UpdateContactView, UpdateFranchiseView, UpdateHomeView, UpdatePackageView,
    UpdateProfileAPI, admin_logout
)

urlpatterns = [
    path('', AdminLoginView.as_view(), name='login'),
    path('logout/', admin_logout, name='logout'),
    path('home/', DashboardView.as_view(), name='home'),
    path('update-profile/', UpdateProfileAPI.as_view(), name='upload_profile'),
    path('package/', DashboardView.as_view(), name='package'),
    path('franchise/', DashboardView.as_view(), name='franchise'),
    path('contact/', DashboardView.as_view(), name='contact'),
    path('home/update/', UpdateHomeView.as_view(), name='update_home'),
    path('dashboard/update-package/', UpdatePackageView.as_view(), name='update_package'),
    path('dashboard/update-contact/', UpdateContactView.as_view(), name='update_contact'),
    path('dashboard/update-franchise/', UpdateFranchiseView.as_view(), name='update_franchise'),
    

    


]
