# resources/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

class ResourceCategory(models.Model):
    """Categories for resources (Lecture Notes, Assignments, Exams, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name from FontAwesome/Lucide")
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default="#083750", help_text="Hex color code")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Resource Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Resource(models.Model):
    FILE_TYPES = (
        ('pdf', 'PDF Document'),
        ('word', 'Word Document'),
        ('excel', 'Excel Spreadsheet'),
        ('powerpoint', 'PowerPoint Presentation'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('archive', 'Archive (ZIP/RAR)'),
        ('other', 'Other'),
    )
    
    DIFFICULTY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('all_levels', 'All Levels'),
    )
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources')
    description = RichTextField(help_text="Detailed description of the resource")
    short_description = models.CharField(max_length=300, blank=True, help_text="Brief summary for cards")
    
    # File Information
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default='pdf')
    file = models.FileField(
        upload_to='resources/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif', 'mp4', 'mp3', 'zip', 'rar'])]
    )
    file_size = models.CharField(max_length=50, blank=True, help_text="e.g., 2.4 MB")
    file_url = models.URLField(blank=True, help_text="External URL for the resource (if not uploaded)")
    
    # Thumbnail/Preview
    thumbnail = models.ImageField(upload_to='resources/thumbnails/', blank=True, null=True)
    
    # Metadata
    author = models.CharField(max_length=200)
    author_email = models.EmailField(blank=True)
    author_bio = models.TextField(blank=True)
    
    # Course Association (optional)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='resources')
    
    # Resource Details
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    duration = models.CharField(max_length=100, blank=True, help_text="Estimated time to consume (e.g., '2 hours', '30 mins')")
    version = models.CharField(max_length=50, blank=True, help_text="Resource version")
    
    # Tags using django-taggit
    tags = TaggableManager(blank=True)
    
    # Statistics
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating_count = models.IntegerField(default=0)
    
    # Display Settings
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    requires_login = models.BooleanField(default=False, help_text="Requires user to be logged in to download")
    order = models.IntegerField(default=0)
    
    # Dates
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-published_date']
        indexes = [
            models.Index(fields=['-downloads']),
            models.Index(fields=['-views']),
            models.Index(fields=['file_type']),
            models.Index(fields=['difficulty_level']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        if self.rating_count > 0:
            return round(self.rating / self.rating_count, 1)
        return 0

class ResourceRating(models.Model):
    """User ratings for resources"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='user_ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resource_ratings')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['resource', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.resource.title} - {self.rating}★"

class ResourceDownload(models.Model):
    """Track resource downloads"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='download_records')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resource_downloads')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.resource.title} - {self.downloaded_at}"

class ResourceCollection(models.Model):
    """Collections/Playlists of resources"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextField(blank=True)
    cover_image = models.ImageField(upload_to='resources/collections/', blank=True, null=True)
    resources = models.ManyToManyField(Resource, related_name='collections')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class UserBookmark(models.Model):
    """User bookmarks for resources"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookmarks')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'resource']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.resource.title}"

class ResourceSearchHistory(models.Model):
    """Track user search history"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=200)
    results_count = models.IntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-searched_at']
        verbose_name_plural = "Resource Search Histories"
    
    def __str__(self):
        return f"{self.user.email} - {self.query}"

class ResourceView(models.Model):
    """Track resource views"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='view_records')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']

class StudyGuide(models.Model):
    """Study guides and supplementary materials"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextField()
    cover_image = models.ImageField(upload_to='resources/study_guides/')
    resources = models.ManyToManyField(Resource, related_name='study_guides')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='study_guides')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title