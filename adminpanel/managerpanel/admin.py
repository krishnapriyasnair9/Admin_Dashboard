from django.contrib import admin
from .models import Banner, Profile

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    # Display all fields in the list view
    list_display = [field.name for field in Banner._meta.fields]
    # Optional: make fields searchable
    search_fields = ('page', 'heading', 'description', 'banner_type')
    # Optional: add filters
    list_filter = ('page', 'banner_type', 'updated_at')
    # Optional: order by updated_at descending
    ordering = ('-updated_at',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Display all fields in the list view
    list_display = [field.name for field in Profile._meta.fields]
    # Optional: make fields searchable
    search_fields = ('user__username',)
    # Optional: add filters
    list_filter = ('user',)
