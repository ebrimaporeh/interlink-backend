# content/models.py
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField

class AboutPage(models.Model):
    """Single model for About page content"""
    title = models.CharField(max_length=200, default="About Interlink Global College")
    subtitle = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to='about/hero/', blank=True, null=True)
    
    # Main content sections
    mission = RichTextField(help_text="Our mission statement")
    vision = RichTextField(help_text="Our vision statement")
    history = RichTextField(blank=True, help_text="Our history and journey")
    
    # Stats section
    stats = models.JSONField(default=list, help_text='[{"number": "1,200", "label": "Graduates"}, ...]')
    
    # Values section
    core_values = models.JSONField(default=list, help_text='[{"title": "Excellence", "description": "...", "icon": "Award"}, ...]')
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "About Page Content"
    
    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

class TeamMember(models.Model):
    """Team members model"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = RichTextField(blank=True)
    image = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    
    # Social links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    # Expertise areas (JSON list)
    expertise = models.JSONField(default=list, help_text='List of expertise areas')
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return self.name

class GalleryCategory(models.Model):
    """Category for gallery items"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Gallery Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, related_name='items')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    
    # Image fields
    image = models.ImageField(upload_to='gallery/images/', blank=True, null=True)
    
    # Video fields (supports YouTube, Vimeo, etc.)
    video_url = EmbedVideoField(blank=True, help_text="YouTube or Vimeo URL")
    video_thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)
    
    # Metadata
    date_taken = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    photographer = models.CharField(max_length=200, blank=True)
    
    # Display settings
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    # Stats
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"
    
    def __str__(self):
        return self.title

class PolicyCategory(models.Model):
    """Category for policies (School, NAQAA, Classroom, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name from FontAwesome/Lucide")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Policy Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Policy(models.Model):
    """Individual policy items"""
    category = models.ForeignKey(PolicyCategory, on_delete=models.CASCADE, related_name='policies')
    title = models.CharField(max_length=200)
    content = RichTextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Policy"
        verbose_name_plural = "Policies"
    
    def __str__(self):
        return f"{self.category.name} - {self.title}"

class Testimonial(models.Model):
    """Student testimonials"""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    course = models.CharField(max_length=200, blank=True, help_text="Course they completed")
    content = models.TextField()
    rating = models.IntegerField(default=5, help_text="Rating from 1-5")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.name} - {self.rating}★"

class BlogCategory(models.Model):
    """Blog categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Blog Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    """Blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    author = models.CharField(max_length=200)
    author_image = models.ImageField(upload_to='blog/authors/', blank=True, null=True)
    author_bio = models.TextField(blank=True)
    
    # Content
    excerpt = models.CharField(max_length=300, help_text="Short summary for cards")
    content = RichTextField()
    featured_image = models.ImageField(upload_to='blog/featured/')
    
    # Metadata
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    read_time = models.IntegerField(default=5, help_text="Estimated read time in minutes")
    
    # Statistics
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    # Display settings
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=500, blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-published_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=300)
    answer = RichTextField()
    category = models.CharField(max_length=100, blank=True, help_text="e.g., Admissions, Courses, Payments")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'category']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question

class Partner(models.Model):
    """Partner organizations"""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Achievement(models.Model):
    """College achievements and milestones"""
    year = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-year', 'order']
    
    def __str__(self):
        return f"{self.year} - {self.title}"
    
class HomepageSettings(models.Model):
    """Model to manage homepage content"""
    title = models.CharField(max_length=200, default="Welcome to Interlink Global College")
    subtitle = models.CharField(max_length=500, blank=True)
    hero_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    
    # Featured content selection (using ManyToMany relationships)
    featured_testimonials = models.ManyToManyField(Testimonial, blank=True, related_name='homepage_featured')
    featured_gallery = models.ManyToManyField(GalleryItem, blank=True, related_name='homepage_featured')
    featured_blog_posts = models.ManyToManyField(BlogPost, blank=True, related_name='homepage_featured')
    featured_team_members = models.ManyToManyField(TeamMember, blank=True, related_name='homepage_featured')
    featured_partners = models.ManyToManyField(Partner, blank=True, related_name='homepage_featured')
    
    # Display limits
    max_testimonials = models.IntegerField(default=3, help_text="Maximum number of testimonials to show")
    max_gallery_items = models.IntegerField(default=8, help_text="Maximum number of gallery items to show")
    max_blog_posts = models.IntegerField(default=3, help_text="Maximum number of blog posts to show")
    max_team_members = models.IntegerField(default=4, help_text="Maximum number of team members to show")
    max_partners = models.IntegerField(default=6, help_text="Maximum number of partners to show")
    
    # Statistics (JSON field)
    stats = models.JSONField(default=list, help_text='[{"number": "1,200", "label": "Graduates"}, ...]')
    
    # Settings
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Homepage Settings"
        verbose_name_plural = "Homepage Settings"
    
    def __str__(self):
        return "Homepage Configuration"