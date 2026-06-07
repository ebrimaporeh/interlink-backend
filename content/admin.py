# content/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AboutPage, TeamMember, GalleryCategory, GalleryItem,
    PolicyCategory, Policy, Testimonial, BlogCategory,
    BlogPost, FAQ, Partner, Achievement, HomepageSettings
)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Main Content', {
            'fields': ('title', 'subtitle', 'hero_image', 'mission', 'vision', 'history')
        }),
        ('Statistics', {
            'fields': ('stats',),
            'classes': ('wide',)
        }),
        ('Core Values', {
            'fields': ('core_values',),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one about page instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active', 'image_preview']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position', 'bio']
    list_editable = ['order', 'is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Photo'

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'item_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'is_featured', 'is_active', 'order', 'image_preview']
    list_filter = ['media_type', 'category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'caption', 'description']
    list_editable = ['order', 'is_featured', 'is_active']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(PolicyCategory)
class PolicyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_active']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'rating', 'is_featured', 'is_active', 'order']
    list_filter = ['rating', 'is_featured', 'is_active']
    search_fields = ['name', 'content', 'course']
    list_editable = ['order', 'is_featured', 'is_active']

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'is_featured', 'views', 'likes', 'image_preview']
    list_filter = ['category', 'is_published', 'is_featured', 'published_at']
    search_fields = ['title', 'content', 'author', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'likes', 'published_at']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'author', 'author_image', 'author_bio')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('tags', 'read_time')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_published', 'is_featured')
        }),
    )
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.featured_image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'order', 'is_active', 'logo_preview']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: contain;" />', obj.logo.url)
        return "No Logo"
    logo_preview.short_description = 'Logo'

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'order', 'is_active']
    list_filter = ['year', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']

@admin.register(HomepageSettings)
class HomepageSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Section', {
            'fields': ('title', 'subtitle', 'hero_image')
        }),
        ('Statistics', {
            'fields': ('stats',),
            'description': 'Format: [{"number": "1,200", "label": "Graduates"}, ...]',
            'classes': ('wide',)
        }),
        ('Featured Content Selection', {
            'fields': (
                'featured_testimonials',
                'featured_gallery',
                'featured_blog_posts',
                'featured_team_members',
                'featured_partners'
            ),
            'description': 'Select which items to display on the homepage',
            'classes': ('wide',)
        }),
        ('Display Limits', {
            'fields': (
                'max_testimonials',
                'max_gallery_items',
                'max_blog_posts',
                'max_team_members',
                'max_partners'
            ),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('is_active', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    list_display = ['title', 'is_active', 'updated_at', 'hero_preview']
    readonly_fields = ['updated_at']
    
    def hero_preview(self, obj):
        if obj.hero_image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.hero_image.url)
        return "No Image"
    hero_preview.short_description = 'Hero Image Preview'
    
    def has_add_permission(self, request):
        # Only allow one homepage settings instance
        if self.model.objects.exists() and not request.GET.get('force'):
            return False
        return super().has_add_permission(request)