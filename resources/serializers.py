# resources/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from taggit.models import Tag
from .models import (
    ResourceCategory, Resource, ResourceRating, ResourceDownload,
    ResourceCollection, UserBookmark, StudyGuide, ResourceView
)

User = get_user_model()

class ResourceCategorySerializer(serializers.ModelSerializer):
    resource_count = serializers.IntegerField(source='resources.count', read_only=True)
    
    class Meta:
        model = ResourceCategory
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at')

class ResourceListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    tags_list = serializers.SerializerMethodField()
    formatted_size = serializers.CharField(source='file_size', read_only=True)
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Resource
        fields = (
            'id', 'title', 'slug', 'short_description', 'file_type', 'file_size', 'file', 'file_url',
            'thumbnail', 'author', 'difficulty_level', 'downloads', 'views',
            'likes', 'rating', 'rating_count', 'average_rating', 'is_featured',
            'published_date', 'category_name', 'category_icon', 'category_color',
            'tags_list', 'formatted_size', 'is_bookmarked'
        )
    
    def get_tags_list(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserBookmark.objects.filter(user=request.user, resource=obj).exists()
        return False

class ResourceDetailSerializer(serializers.ModelSerializer):
    # Nested read for display; category FK is writable as integer via the default field
    category_detail = ResourceCategorySerializer(source='category', read_only=True)
    tags_list = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    related_resources = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = '__all__'
        read_only_fields = (
            'slug', 'downloads', 'views', 'likes',
            'rating', 'rating_count', 'published_date', 'updated_date',
        )
        extra_kwargs = {
            'file':        {'required': False, 'allow_null': True},
            'thumbnail':   {'required': False, 'allow_null': True},
            'file_url':    {'required': False, 'allow_blank': True},
            'author':      {'required': False, 'allow_blank': True},
            'category':    {'required': False, 'allow_null': True},
        }

    def get_tags_list(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = ResourceRating.objects.filter(resource=obj, user=request.user).first()
            if rating:
                return {'rating': rating.rating, 'review': rating.review}
        return None

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserBookmark.objects.filter(user=request.user, resource=obj).exists()
        return False

    def get_related_resources(self, obj):
        from django.db.models import Q
        tags = obj.tags.all()
        related = Resource.objects.filter(
            Q(category=obj.category) | Q(tags__in=tags),
            is_active=True,
        ).exclude(id=obj.id).distinct()[:5]
        return ResourceListSerializer(related, many=True, context=self.context).data

class ResourceRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = ResourceRating
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        rating, created = ResourceRating.objects.update_or_create(
            resource=validated_data['resource'],
            user=validated_data['user'],
            defaults={'rating': validated_data['rating'], 'review': validated_data.get('review', '')}
        )
        
        # Update resource average rating
        resource = rating.resource
        ratings = ResourceRating.objects.filter(resource=resource)
        resource.rating = sum(r.rating for r in ratings)
        resource.rating_count = ratings.count()
        resource.save(update_fields=['rating', 'rating_count'])
        
        return rating

class ResourceDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceDownload
        fields = '__all__'
        read_only_fields = ('id', 'user', 'ip_address', 'user_agent', 'downloaded_at')

class ResourceCollectionSerializer(serializers.ModelSerializer):
    resource_count = serializers.IntegerField(source='resources.count', read_only=True)
    resources = ResourceListSerializer(many=True, read_only=True)
    
    class Meta:
        model = ResourceCollection
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')

class UserBookmarkSerializer(serializers.ModelSerializer):
    resource_details = ResourceListSerializer(source='resource', read_only=True)
    
    class Meta:
        model = UserBookmark
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class StudyGuideSerializer(serializers.ModelSerializer):
    resources = ResourceListSerializer(many=True, read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = StudyGuide
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']

class ResourceStatsSerializer(serializers.Serializer):
    total_resources = serializers.IntegerField()
    total_downloads = serializers.IntegerField()
    total_views = serializers.IntegerField()
    top_categories = serializers.ListField()
    popular_tags = serializers.ListField()