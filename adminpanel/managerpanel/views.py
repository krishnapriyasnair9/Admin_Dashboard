from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Banner

#Login view (superuser only)
class AdminLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        return '/dashboard/'

#Logout
def admin_logout(request):
    logout(request)
    return redirect('/')

#Superuser-only access mixin
class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        
        return redirect('/login/')

#Dashboard (list all banners)
class DashboardView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def get(self, request):
        banners = Banner.objects.all().order_by('page')
        return render(request, 'dashboard.html', {'banners': banners})


#Create/Update Banner
class BannerUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def post(self, request):
        page = request.POST.get('page')
        banner_type = request.POST.get('banner_type')
        banner_file = request.FILES.get('banner_file')

        #Validate input
        if not all([page, banner_type, banner_file]):
            messages.error(request, "Please fill all fields and upload a file before updating.")
            return redirect('/dashboard/')

        #Validate file type
        valid_type = banner_file.content_type.startswith(banner_type)
        if not valid_type:
            messages.error(request, f"Your type is {banner_type}, please upload a {banner_type} file!")
            return redirect('/dashboard/')

        #Create or update the banner
        banner, _ = Banner.objects.get_or_create(page=page)
        banner.banner_type = banner_type
        banner.image = banner_file if banner_type == 'image' else None
        banner.video = banner_file if banner_type == 'video' else None
        banner.save()

        #Success message
        messages.success(request, f"{page.capitalize()} banner updated successfully!")
        return redirect('/dashboard/')
