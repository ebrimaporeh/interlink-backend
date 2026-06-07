# courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseCategoryViewSet, CourseViewSet, CourseModuleViewSet,
    CourseLessonViewSet, EnrollmentViewSet, CourseReviewViewSet,
    MyCoursesView, CertificateVerificationView, CourseStatsView,
)

router = DefaultRouter()
router.register(r'categories',  CourseCategoryViewSet, basename='course-category')
router.register(r'modules',     CourseModuleViewSet,   basename='course-module')
router.register(r'lessons',     CourseLessonViewSet,   basename='course-lesson')
router.register(r'enrollments', EnrollmentViewSet,     basename='enrollment')
router.register(r'reviews',     CourseReviewViewSet,   basename='course-review')
# Register courses last — its lookup regex is broad ([\w-]+) and must not shadow
# the fixed-prefix routes above.
router.register(r'', CourseViewSet, basename='course')

urlpatterns = [
    # Fixed-path views — listed BEFORE router.urls so they are matched first
    path('stats/',       CourseStatsView.as_view(),         name='course-stats'),
    path('my-courses/',  MyCoursesView.as_view(),           name='my-courses'),
    path('certificates/verify/<str:certificate_number>/',
         CertificateVerificationView.as_view(),             name='verify-certificate'),

    # All ViewSet routes
    path('', include(router.urls)),
]
