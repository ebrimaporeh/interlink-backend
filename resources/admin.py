# resources/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ResourceCategory, Resource, ResourceRating, ResourceDownload,
    ResourceCollection, UserBookmark, StudyGuide, ResourceView,
    ResourceSearchHistory
)

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color', 'order', 'is_active', 'resource_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    
    def resource_count(self, obj):
        return obj.resources.count()
    resource_count.short_description = 'Resources'

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'file_type', 'author', 'downloads', 'views', 'is_featured', 'is_active', 'thumbnail_preview']
    list_filter = ['category', 'file_type', 'difficulty_level', 'is_featured', 'is_active', 'published_date']
    search_fields = ['title', 'description', 'author']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['downloads', 'views', 'likes', 'rating', 'rating_count', 'published_date', 'updated_date']
    list_editable = ['is_featured', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description', 'short_description')
        }),
        ('File Information', {
            'fields': ('file_type', 'file', 'file_size', 'file_url', 'thumbnail')
        }),
        ('Metadata', {
            'fields': ('author', 'author_email', 'author_bio', 'course')
        }),
        ('Resource Details', {
            'fields': ('difficulty_level', 'duration', 'version', 'tags')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'requires_login', 'order')
        }),
        ('Statistics', {
            'fields': ('downloads', 'views', 'likes', 'rating', 'rating_count'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('published_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.thumbnail.url)
        return "No Preview"
    thumbnail_preview.short_description = 'Preview'

@admin.register(ResourceRating)
class ResourceRatingAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'rating', 'review_preview', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['resource__title', 'user__email', 'review']
    
    def review_preview(self, obj):
        return obj.review[:50] + '...' if len(obj.review) > 50 else obj.review
    review_preview.short_description = 'Review'

@admin.register(ResourceDownload)
class ResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'ip_address', 'downloaded_at']
    list_filter = ['downloaded_at']
    search_fields = ['resource__title', 'user__email', 'ip_address']
    readonly_fields = ['downloaded_at']

@admin.register(ResourceCollection)
class ResourceCollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'resource_count']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'is_active']
    filter_horizontal = ['resources']
    
    def resource_count(self, obj):
        return obj.resources.count()
    resource_count.short_description = 'Resources'

@admin.register(UserBookmark)
class UserBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'resource__title']

@admin.register(StudyGuide)
class StudyGuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_active', 'resource_count']
    list_filter = ['is_active', 'course']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'is_active']
    filter_horizontal = ['resources']
    
    def resource_count(self, obj):
        return obj.resources.count()
    resource_count.short_description = 'Resources'

@admin.register(ResourceView)
class ResourceViewAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['resource__title', 'user__email', 'ip_address']

@admin.register(ResourceSearchHistory)
class ResourceSearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'results_count', 'searched_at']
    list_filter = ['searched_at']
    search_fields = ['user__email', 'query']