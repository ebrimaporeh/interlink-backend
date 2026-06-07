# content/serializers.py
from rest_framework import serializers
from .models import (
    AboutPage, TeamMember, GalleryCategory, GalleryItem,
    PolicyCategory, Policy, Testimonial, BlogCategory,
    BlogPost, FAQ, Partner, Achievement
)


class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
        }


class GalleryCategorySerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(source='items.count', read_only=True)

    class Meta:
        model = GalleryCategory
        fields = '__all__'
        # slug is auto-generated from name in model.save()
        read_only_fields = ('id', 'slug')


class GalleryItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    video_embed_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryItem
        fields = '__all__'
        read_only_fields = ('views', 'likes', 'created_at', 'updated_at')
        extra_kwargs = {
            'title':            {'required': False, 'allow_blank': True},
            'image':            {'required': False, 'allow_null': True},
            'video_thumbnail':  {'required': False, 'allow_null': True},
            'category':         {'required': False, 'allow_null': True},
        }

    def get_video_embed_url(self, obj):
        return str(obj.video_url) if obj.video_url else None

    def validate(self, data):
        # Auto-fill title from caption if not provided
        if not data.get('title') and data.get('caption'):
            data['title'] = data['caption']
        return data


class PolicyCategorySerializer(serializers.ModelSerializer):
    policy_count = serializers.IntegerField(source='policies.count', read_only=True)

    class Meta:
        model = PolicyCategory
        fields = '__all__'
        read_only_fields = ('id', 'slug')


class PolicySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Policy
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'category': {'required': False, 'allow_null': True},
        }


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        read_only_fields = ('created_at',)
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
        }


class BlogCategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = BlogCategory
        fields = '__all__'
        read_only_fields = ('id', 'slug')


class BlogPostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = (
            'id', 'title', 'slug', 'excerpt', 'featured_image', 'author',
            'read_time', 'views', 'likes', 'is_featured', 'published_at',
            'category_name', 'formatted_date',
        )

    def get_formatted_date(self, obj):
        return obj.published_at.strftime("%b %d, %Y")


class BlogPostDetailSerializer(serializers.ModelSerializer):
    # Nested read for display; category FK is writable as integer via the default field
    category_detail = BlogCategorySerializer(source='category', read_only=True)
    tags_list = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = (
            # Auto-generated or auto-set — never sent by the client
            'slug', 'author', 'views', 'likes', 'published_at', 'updated_at',
        )
        extra_kwargs = {
            # Images and category are optional so partial submissions work
            'featured_image': {'required': False, 'allow_null': True},
            'author_image':   {'required': False, 'allow_null': True},
            'category':       {'required': False, 'allow_null': True},
        }

    def get_tags_list(self, obj):
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',')]
        return []

    def get_formatted_date(self, obj):
        return obj.published_at.strftime("%B %d, %Y")


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'
        extra_kwargs = {
            'logo': {'required': False, 'allow_null': True},
        }


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'