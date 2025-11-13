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
        hero_heading = request.POST.get("heading", "").strip()
        hero_description = request.POST.get("description", "").strip()
        banner_type = request.POST.get("banner_type", "")
        banner_file = request.FILES.get("banner_file")

        if not (hero_heading or hero_description or banner_type or banner_file):
            messages.error(request, "⚠️ Please fill at least one field before saving.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))

        if banner_file and not banner_type:
            messages.error(request, "❌ Banner file uploaded but banner type not selected. Please choose 'Image' or 'Video'.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))

        if banner_file and banner_type:
            ext = banner_file.name.split(".")[-1].lower()
            if banner_type == "video" and ext not in ["mp4", "webm", "mov", "ogg"]:
                messages.error(request, "❌ Invalid video format. Please upload MP4, WEBM, MOV, or OGG.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))
            elif banner_type == "image" and ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                messages.error(request, "❌ Invalid image format. Please upload JPG, PNG, GIF, or WEBP.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))

        banner, _ = Banner.objects.get_or_create(page="home")

        updated_fields = []
        if hero_heading:
            banner.heading = hero_heading
            updated_fields.append("heading")
        if hero_description:
            banner.description = hero_description
            updated_fields.append("description")
        if banner_type:
            banner.banner_type = banner_type
            updated_fields.append("banner_type")
        if banner_file:
            banner.banner_file = banner_file
            updated_fields.append("banner_file")

        if not updated_fields:
            messages.warning(request, "⚠️ No changes detected. Please edit something before saving.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))

        banner.save()
        messages.success(request, f"✅ Home page updated successfully ({', '.join(updated_fields)} updated).")
        return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=home"))


# =========================================
# 🔹 2. PACKAGE PAGE UPDATE VIEW
# =========================================
class UpdatePackageView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def post(self, request):
        heading = request.POST.get("heading", "").strip()
        description = request.POST.get("description", "").strip()
        banner_type = request.POST.get("banner_type", "")
        banner_file = request.FILES.get("banner_file")

        if not (heading or description or banner_type or banner_file):
            messages.error(request, "⚠️ Please fill at least one field before saving.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))

        if banner_file and not banner_type:
            messages.error(request, "❌ Banner file uploaded but banner type not selected.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))

        if banner_file and banner_type:
            ext = banner_file.name.split(".")[-1].lower()
            if banner_type == "video" and ext not in ["mp4", "webm", "mov", "ogg"]:
                messages.error(request, "❌ Invalid video format for package banner.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))
            elif banner_type == "image" and ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                messages.error(request, "❌ Invalid image format for package banner.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))

        banner, _ = Banner.objects.get_or_create(page="package")

        updated_fields = []
        if heading:
            banner.heading = heading
            updated_fields.append("heading")
        if description:
            banner.description = description
            updated_fields.append("description")
        if banner_type:
            banner.banner_type = banner_type
            updated_fields.append("banner_type")
        if banner_file:
            banner.banner_file = banner_file
            updated_fields.append("banner_file")

        if not updated_fields:
            messages.warning(request, "⚠️ No changes detected.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))

        banner.save()
        messages.success(request, f"✅ Package page updated successfully ({', '.join(updated_fields)} updated).")
        return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=package"))


# =========================================
# 🔹 3. FRANCHISE PAGE UPDATE VIEW
# =========================================
class UpdateFranchiseView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def post(self, request):
        heading = request.POST.get("heading", "").strip()
        description = request.POST.get("description", "").strip()
        banner_type = request.POST.get("banner_type", "")
        banner_file = request.FILES.get("banner_file")

        if not (heading or description or banner_type or banner_file):
            messages.error(request, "⚠️ Please fill at least one field before saving.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))

        if banner_file and not banner_type:
            messages.error(request, "❌ Banner file uploaded but banner type not selected.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))

        if banner_file and banner_type:
            ext = banner_file.name.split(".")[-1].lower()
            if banner_type == "video" and ext not in ["mp4", "webm", "mov", "ogg"]:
                messages.error(request, "❌ Invalid video format for franchise banner.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))
            elif banner_type == "image" and ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                messages.error(request, "❌ Invalid image format for franchise banner.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))

        banner, _ = Banner.objects.get_or_create(page="franchise")

        updated_fields = []
        if heading:
            banner.heading = heading
            updated_fields.append("heading")
        if description:
            banner.description = description
            updated_fields.append("description")
        if banner_type:
            banner.banner_type = banner_type
            updated_fields.append("banner_type")
        if banner_file:
            banner.banner_file = banner_file
            updated_fields.append("banner_file")

        if not updated_fields:
            messages.warning(request, "⚠️ No changes detected.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))

        banner.save()
        messages.success(request, f"✅ Franchise page updated successfully ({', '.join(updated_fields)} updated).")
        return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=franchise"))


# =========================================
# 🔹 4. CONTACT PAGE UPDATE VIEW
# =========================================
class UpdateContactView(LoginRequiredMixin, SuperUserRequiredMixin, View):
    def post(self, request):
        heading = request.POST.get("heading", "").strip()
        description = request.POST.get("description", "").strip()
        banner_type = request.POST.get("banner_type", "")
        banner_file = request.FILES.get("banner_file")

        if not (heading or description or banner_type or banner_file):
            messages.error(request, "⚠️ Please fill at least one field before saving.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))

        if banner_file and not banner_type:
            messages.error(request, "❌ Banner file uploaded but banner type not selected.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))

        if banner_file and banner_type:
            ext = banner_file.name.split(".")[-1].lower()
            if banner_type == "video" and ext not in ["mp4", "webm", "mov", "ogg"]:
                messages.error(request, "❌ Invalid video format for contact banner.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))
            elif banner_type == "image" and ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                messages.error(request, "❌ Invalid image format for contact banner.")
                return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))

        banner, _ = Banner.objects.get_or_create(page="contact")

        updated_fields = []
        if heading:
            banner.heading = heading
            updated_fields.append("heading")
        if description:
            banner.description = description
            updated_fields.append("description")
        if banner_type:
            banner.banner_type = banner_type
            updated_fields.append("banner_type")
        if banner_file:
            banner.banner_file = banner_file
            updated_fields.append("banner_file")

        if not updated_fields:
            messages.warning(request, "⚠️ No changes detected.")
            return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))

        banner.save()
        messages.success(request, f"✅ Contact page updated successfully ({', '.join(updated_fields)} updated).")
        return redirect(request.META.get("HTTP_REFERER", "/dashboard/?page=contact"))