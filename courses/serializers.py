# courses/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models  # Add this import
from .models import (
    CourseCategory, Course, CourseModule, CourseLesson, 
    Enrollment, CourseReview, Certificate
)

User = get_user_model()

class CourseCategorySerializer(serializers.ModelSerializer):
    course_count = serializers.IntegerField(source='courses.count', read_only=True)
    
    class Meta:
        model = CourseCategory
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')

class CourseModuleSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lessons.count', read_only=True)
    
    class Meta:
        model = CourseModule
        fields = '__all__'

class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)  # Remove source
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = (
            'id', 'title', 'slug', 'level', 'short_description', 'duration', 
            'price', 'image', 'banner_icon', 'is_featured', 'order', 
            'category_name', 'category_slug', 'enrollment_count', 'average_rating'
        )
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

class CourseDetailSerializer(serializers.ModelSerializer):
    # Nested read for display; category FK is writable as integer via the default field
    category_detail = CourseCategorySerializer(source='category', read_only=True)
    modules = CourseModuleSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    enrollment_count = serializers.IntegerField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')
        extra_kwargs = {
            'image':             {'required': False, 'allow_null': True},
            'category':          {'required': False, 'allow_null': True},
            'short_description': {'required': False, 'allow_blank': True},
        }

    def get_reviews(self, obj):
        reviews = obj.reviews.filter(is_approved=True)[:10]
        return CourseReviewSerializer(reviews, many=True).data

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(
                student=request.user,
                course=obj,
                status__in=['confirmed', 'in_progress', 'completed'],
            ).exists()
        return False

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            enrollment = Enrollment.objects.filter(student=request.user, course=obj).first()
            if enrollment:
                return {
                    'status': enrollment.status,
                    'progress': enrollment.progress_percentage,
                    'started_at': enrollment.started_at,
                    'completed_at': enrollment.completed_at,
                }
        return None

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    course_image = serializers.ImageField(source='course.image', read_only=True)
    progress = serializers.IntegerField(source='progress_percentage', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('id', 'enrollment_date', 'student', 'progress_percentage', 'certificate_issued')

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('course', 'notes')
    
    def validate(self, data):
        course = data['course']
        if not course.is_active:
            raise serializers.ValidationError({"course": "This course is not currently active"})
        
        if course.is_full:
            raise serializers.ValidationError({"course": "This course is full"})
        
        user = self.context['request'].user
        if Enrollment.objects.filter(student=user, course=course).exists():
            raise serializers.ValidationError({"course": "You are already enrolled in this course"})
        
        return data
    
    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        validated_data['status'] = 'pending'
        return super().create(validated_data)

class CourseReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_avatar = serializers.ImageField(source='student.profile.profile_picture', read_only=True)
    
    class Meta:
        model = CourseReview
        fields = '__all__'
        read_only_fields = ('id', 'student', 'created_at', 'updated_at', 'is_approved')
    
    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)

class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='enrollment.student.get_full_name', read_only=True)
    student_email = serializers.CharField(source='enrollment.student.email', read_only=True)
    course_title = serializers.CharField(source='enrollment.course.title', read_only=True)
    
    class Meta:
        model = Certificate
        fields = '__all__'