from django.contrib import admin
from django.utils.html import format_html
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('page', 'banner_type', 'image_preview', 'video_preview', 'updated_at')
    list_filter = ('page', 'banner_type')
    search_fields = ('page',)

    readonly_fields = ('image_preview', 'video_preview')

    # Show image preview
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'

    # Show video preview
    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="150" controls>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>', obj.video.url
            )
        return "-"
    video_preview.short_description = 'Video'

    # Ensure all page choices are always visible
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Reset choices for the page field
        form.base_fields['page'].choices = Banner.PAGE_CHOICES
        return form
