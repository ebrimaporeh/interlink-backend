# courses/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CourseCategory, Course, CourseModule, CourseLesson,
    Enrollment, CourseReview, Certificate
)

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'course_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'Courses'

class CourseLessonInline(admin.TabularInline):
    model = CourseLesson
    extra = 1
    fields = ['title', 'order', 'duration_minutes', 'is_free_preview']

class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1
    fields = ['title', 'order', 'duration_hours']
    inlines = [CourseLessonInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'category', 'price', 'is_featured', 'is_active', 'order', 'image_preview']
    list_filter = ['level', 'category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'short_description', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'enrollment_count']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'level', 'short_description', 'description')
        }),
        ('Course Details', {
            'fields': ('duration', 'price', 'price_number', 'modules', 'learning_outcomes', 'prerequisites')
        }),
        ('Media', {
            'fields': ('image', 'banner_icon', 'video_intro')
        }),
        ('Enrollment', {
            'fields': ('max_students', 'current_students', 'start_date', 'end_date')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    inlines = [CourseModuleInline]
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    def enrollment_count(self, obj):
        return obj.enrollment_count
    enrollment_count.short_description = 'Enrollments'

@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_hours']
    list_filter = ['course']
    search_fields = ['title', 'course__title']
    inlines = [CourseLessonInline]

@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'duration_minutes', 'is_free_preview']
    list_filter = ['module__course', 'is_free_preview']
    search_fields = ['title', 'content']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'payment_status', 'enrollment_date', 'progress_percentage']
    list_filter = ['status', 'payment_status', 'enrollment_date']
    search_fields = ['student__email', 'student__username', 'course__title']
    readonly_fields = ['enrollment_date', 'progress_percentage']
    fieldsets = (
        ('Enrollment Info', {
            'fields': ('student', 'course', 'status', 'enrollment_date')
        }),
        ('Payment', {
            'fields': ('payment_status', 'payment_amount', 'payment_date', 'payment_receipt')
        }),
        ('Progress', {
            'fields': ('progress_percentage', 'completed_lessons', 'started_at', 'completed_at')
        }),
        ('Certificate', {
            'fields': ('certificate_issued', 'certificate_number')
        }),
        ('Additional', {
            'fields': ('notes',)
        })
    )

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['course__title', 'student__email', 'comment']
    actions = ['approve_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Approve selected reviews'

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'enrollment', 'issue_date']
    search_fields = ['certificate_number', 'enrollment__student__email']
    readonly_fields = ['certificate_number', 'issue_date']