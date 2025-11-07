from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Banner, Profile


class AdminLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/home/'


def admin_logout(request):
    logout(request)
    return redirect('/')


class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    def handle_no_permission(self):
        return redirect('/')


class DashboardView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def get(self, request):
        # Get which page to show; default = 'home'
        page = request.GET.get("page", "home")

        # Load banners for this page
        banners = Banner.objects.filter(page=page)

        # Get or create user profile
        profile, _ = Profile.objects.get_or_create(user=request.user)

        # Map pages to templates
        page_templates = {
            'home': 'home.html',
            'package': 'package.html',
            'franchise': 'franchise.html',
            'contact': 'contact.html',
        }

        # Choose template for this page; fallback to home.html
        template_name = page_templates.get(page, 'home.html')

        return render(request, template_name, {
            'banners': banners,
            'profile': profile,
            'current_page': page  # for sidebar highlight
        })

class UpdateProfileAPI(LoginRequiredMixin, View):
    login_url = '/'  # Redirect if not logged in

    def post(self, request):
        # Get or create profile
        profile, _ = Profile.objects.get_or_create(user=request.user)

        # File input must have name="photo"
        uploaded_file = request.FILES.get("photo")
        if uploaded_file:
            profile.photo = uploaded_file
            profile.save()
            messages.success(request, "✅ Profile photo updated successfully!")
        else:
            messages.warning(request, "⚠️ No file selected for upload!")

        # Redirect back to the page
        return redirect(request.META.get("HTTP_REFERER", "/home/"))
class UpdateHomeView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def post(self, request):
        hero_heading = request.POST.get("heading")
        hero_description = request.POST.get("description")
        banner_type = request.POST.get("banner_type")  # Must be 'image' or 'video'
        banner_file = request.FILES.get("banner_file")

        # Check if banner type is selected
        if not banner_type:
            messages.error(request, "⚠️ Please select a banner type before saving!")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))

        # Validate file based on selected banner type
        if banner_type == "video":
            if not banner_file or banner_file.name.split('.')[-1].lower() not in ["mp4", "webm"]:
                messages.error(request, "❌ You selected 'Video' but uploaded file is missing or not a valid video!")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))
        elif banner_type == "image":
            if banner_file and banner_file.name.split('.')[-1].lower() not in ["jpg","jpeg","png","gif"]:
                messages.error(request, "❌ You selected 'Image' but uploaded file is not a valid image!")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))

        # Save banner
        banner, _ = Banner.objects.get_or_create(page="home")
        banner.heading = hero_heading
        banner.description = hero_description
        banner.banner_type = banner_type

        if banner_file:
            banner.banner_file = banner_file

        banner.save()
        messages.success(request, "✅ Home page updated successfully!")
        return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))
class UpdatePackageView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def post(self, request):
        # Hero heading & description
        hero_heading = request.POST.get("heading")
        hero_description = request.POST.get("description")

        # Banner type & file
        banner_type = request.POST.get("banner_type")
        banner_file = request.FILES.get("banner_file")

        # Validation: ensure banner type is selected
        if not banner_type:
            messages.error(request, "⚠️ Please select a banner type before saving!")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))

        # Validation: ensure uploaded file matches selected type
        if banner_file:
            ext = banner_file.name.split(".")[-1].lower()
            if banner_type == "image" and ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                messages.error(request, "❌ Uploaded file is not an image. Please select a correct file.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))
            elif banner_type == "video" and ext not in ["mp4", "webm", "mov", "ogg"]:
                messages.error(request, "❌ Uploaded file is not a video. Please select a correct file.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))

        # Save banner (page="package")
        banner, _ = Banner.objects.get_or_create(page="package")
        banner.banner_type = banner_type
        banner.heading = hero_heading
        banner.description = hero_description

        if banner_file:
            banner.banner_file = banner_file

        banner.save()

        messages.success(request, "✅ Package page updated successfully!")
        return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))
class UpdateContactView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def post(self, request):
        # Hero heading & description
        hero_heading = request.POST.get("heading")
        hero_description = request.POST.get("description")

        # Banner type & file
        banner_type = request.POST.get("banner_type")
        banner_file = request.FILES.get("banner_file")

        # Validation: ensure banner type is selected
        if not banner_type:
            messages.error(request, "⚠️ Please select a banner type before saving!")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))

        # Validation: file type matches banner type
        if banner_file:
            ext = banner_file.name.split(".")[-1].lower()
            if banner_type == "image" and ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                messages.error(request, "❌ Uploaded file is not an image. Please select a correct file.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))
            elif banner_type == "video" and ext not in ["mp4", "webm", "mov", "ogg"]:
                messages.error(request, "❌ Uploaded file is not a video. Please select a correct file.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))

        # Save banner (page="contact")
        banner, _ = Banner.objects.get_or_create(page="contact")
        banner.banner_type = banner_type
        banner.heading = hero_heading
        banner.description = hero_description

        if banner_file:
            banner.banner_file = banner_file

        banner.save()
        messages.success(request, "✅ Contact page updated successfully!")
        return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))
class UpdateFranchiseView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def post(self, request):
        # Hero heading & description
        hero_heading = request.POST.get("heading")
        hero_description = request.POST.get("description")

        # Banner type & file
        banner_type = request.POST.get("banner_type")
        banner_file = request.FILES.get("banner_file")

        # Validation: ensure banner type is selected
        if not banner_type:
            messages.error(request, "⚠️ Please select a banner type before saving!")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))

        # Validation: file type matches banner type
        if banner_file:
            ext = banner_file.name.split(".")[-1].lower()
            if banner_type == "image" and ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                messages.error(request, "❌ Uploaded file is not an image. Please select a correct file.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))
            elif banner_type == "video" and ext not in ["mp4", "webm", "mov", "ogg"]:
                messages.error(request, "❌ Uploaded file is not a video. Please select a correct file.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))

        # Save banner (page="franchise")
        banner, _ = Banner.objects.get_or_create(page="franchise")
        banner.banner_type = banner_type
        banner.heading = hero_heading
        banner.description = hero_description

        if banner_file:
            banner.banner_file = banner_file

        banner.save()
        messages.success(request, "✅ Franchise page updated successfully!")
        return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))
