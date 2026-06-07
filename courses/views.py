# courses/views.py
from rest_framework import viewsets, permissions, filters, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from django.utils import timezone
from .models import (
    CourseCategory, Course, CourseModule, CourseLesson,
    Enrollment, CourseReview, Certificate
)
from .serializers import (
    CourseCategorySerializer, CourseListSerializer, CourseDetailSerializer,
    CourseModuleSerializer, CourseLessonSerializer, EnrollmentSerializer,
    EnrollmentCreateSerializer, CourseReviewSerializer, CertificateSerializer
)

MULTIPART = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff or request.user.is_superuser:
            return True
        try:
            return request.user.profile.role in ('admin', 'staff')
        except Exception:
            return False


def _is_admin(request):
    if not request.user or not request.user.is_authenticated:
        return False
    if request.user.is_staff or request.user.is_superuser:
        return True
    try:
        return request.user.profile.role in ('admin', 'staff')
    except Exception:
        return False


# ── Course Categories ─────────────────────────────────────────────────────────
class CourseCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name']

    def get_queryset(self):
        if _is_admin(self.request):
            return CourseCategory.objects.all()
        return CourseCategory.objects.filter(is_active=True)


# ── Courses ───────────────────────────────────────────────────────────────────
class CourseViewSet(viewsets.ModelViewSet):
    """
    Supports slug (public) and integer PK (admin) in the same URL pattern.
    GET  /courses/my-course-slug/   → public detail
    GET  /courses/5/                → detail by pk
    PATCH /courses/5/               → admin update
    DELETE /courses/5/              → admin delete
    """
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = MULTIPART
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'category__slug', 'is_featured', 'is_active']
    search_fields = ['title', 'short_description', 'description']
    ordering_fields = ['price', 'created_at', 'order', 'title']
    lookup_field = 'pk'
    lookup_value_regex = r'[\w-]+'

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update', 'partial_update'):
            return CourseDetailSerializer
        return CourseListSerializer

    def get_queryset(self):
        qs = Course.objects.all() if _is_admin(self.request) else Course.objects.filter(is_active=True)
        if not _is_admin(self.request):
            level = self.request.query_params.get('level')
            if level:
                qs = qs.filter(level=level)
            category = self.request.query_params.get('category')
            if category:
                qs = qs.filter(category__slug=category)
            if self.request.query_params.get('featured') == 'true':
                qs = qs.filter(is_featured=True)
        return qs

    def get_object(self):
        pk_or_slug = self.kwargs.get('pk')
        qs = self.get_queryset()
        if str(pk_or_slug).isdigit():
            obj = get_object_or_404(qs, pk=pk_or_slug)
        else:
            obj = get_object_or_404(qs, slug=pk_or_slug)
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['get', 'post'], url_path='modules')
    def modules(self, request, pk=None):
        course = self.get_object()
        if request.method == 'GET':
            modules = CourseModule.objects.filter(course=course).prefetch_related('lessons')
            return Response(CourseModuleSerializer(modules, many=True, context={'request': request}).data)
        # POST — admin creates a module
        if not _is_admin(request):
            return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CourseModuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], url_path='reviews')
    def reviews(self, request, pk=None):
        course = self.get_object()
        if request.method == 'GET':
            reviews = CourseReview.objects.filter(course=course, is_approved=True)
            return Response(CourseReviewSerializer(reviews, many=True, context={'request': request}).data)
        if not request.user.is_authenticated:
            return Response({'detail': 'Login required.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CourseReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ── Course Modules ────────────────────────────────────────────────────────────
class CourseModuleViewSet(viewsets.ModelViewSet):
    serializer_class = CourseModuleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = CourseModule.objects.all()
        course_slug = self.request.query_params.get('course')
        if course_slug:
            qs = qs.filter(course__slug=course_slug)
        return qs

    @action(detail=True, methods=['get', 'post'], url_path='lessons')
    def lessons(self, request, pk=None):
        module = self.get_object()
        if request.method == 'GET':
            lessons = CourseLesson.objects.filter(module=module)
            return Response(CourseLessonSerializer(lessons, many=True, context={'request': request}).data)
        if not _is_admin(request):
            return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CourseLessonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(module=module)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ── Course Lessons ────────────────────────────────────────────────────────────
class CourseLessonViewSet(viewsets.ModelViewSet):
    serializer_class = CourseLessonSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = CourseLesson.objects.all()
        module_id = self.request.query_params.get('module')
        if module_id:
            qs = qs.filter(module_id=module_id)
        return qs


# ── Enrollments ───────────────────────────────────────────────────────────────
class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        return EnrollmentSerializer

    def get_queryset(self):
        if _is_admin(self.request):
            return Enrollment.objects.all().select_related('course', 'student')
        return Enrollment.objects.filter(student=self.request.user).select_related('course')

    @action(detail=True, methods=['post'], url_path=r'progress/(?P<lesson_id>\d+)')
    def progress(self, request, pk=None, lesson_id=None):
        enrollment = self.get_object()
        lesson = get_object_or_404(CourseLesson, id=lesson_id)
        lesson_id_int = int(lesson_id)

        if lesson_id_int not in enrollment.completed_lessons:
            enrollment.completed_lessons.append(lesson_id_int)
            total = CourseLesson.objects.filter(module__course=enrollment.course).count()
            if total > 0:
                enrollment.progress_percentage = min(int(len(enrollment.completed_lessons) / total * 100), 100)
            if enrollment.status == 'confirmed' and enrollment.progress_percentage > 0:
                enrollment.status = 'in_progress'
                enrollment.started_at = timezone.now()
            if enrollment.progress_percentage == 100:
                enrollment.status = 'completed'
                enrollment.completed_at = timezone.now()
            enrollment.save()

        return Response({
            'progress': enrollment.progress_percentage,
            'completed_lessons': enrollment.completed_lessons,
            'status': enrollment.status,
        })


# ── Course Reviews ────────────────────────────────────────────────────────────
class CourseReviewViewSet(viewsets.ModelViewSet):
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if _is_admin(self.request):
            return CourseReview.objects.all()
        return CourseReview.objects.filter(is_approved=True)


# ── My Courses (shortcut) ─────────────────────────────────────────────────────
class MyCoursesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Enrollment.objects.filter(student=request.user)
        status_filter = request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return Response(EnrollmentSerializer(qs, many=True, context={'request': request}).data)


# ── Certificate Verification ──────────────────────────────────────────────────
class CertificateVerificationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, certificate_number):
        try:
            cert = Certificate.objects.get(certificate_number=certificate_number)
            return Response({'valid': True, 'certificate': CertificateSerializer(cert).data})
        except Certificate.DoesNotExist:
            return Response({'valid': False, 'message': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)


# ── Course Stats ──────────────────────────────────────────────────────────────
class CourseStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'total_courses':    Course.objects.filter(is_active=True).count(),
            'total_students':   Enrollment.objects.filter(status__in=['confirmed', 'in_progress', 'completed']).values('student').distinct().count(),
            'total_categories': CourseCategory.objects.filter(is_active=True).count(),
            'average_rating':   CourseReview.objects.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg'] or 0,
        })
