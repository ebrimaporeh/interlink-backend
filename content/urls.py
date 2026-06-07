# content/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AboutPageView, HomepageDataView,
    TeamMemberViewSet, GalleryCategoryViewSet, GalleryItemViewSet,
    PolicyCategoryViewSet, PolicyViewSet, TestimonialViewSet,
    BlogCategoryViewSet, BlogPostViewSet, FAQViewSet,
    PartnerViewSet, AchievementViewSet,
)

router = DefaultRouter()
router.register(r'team',                 TeamMemberViewSet,      basename='team')
router.register(r'gallery/categories',   GalleryCategoryViewSet, basename='gallery-category')
router.register(r'gallery',              GalleryItemViewSet,     basename='gallery')
router.register(r'policies/categories',  PolicyCategoryViewSet,  basename='policy-category')
router.register(r'policies',             PolicyViewSet,          basename='policy')
router.register(r'testimonials',         TestimonialViewSet,     basename='testimonial')
router.register(r'blog/categories',      BlogCategoryViewSet,    basename='blog-category')
router.register(r'blog',                 BlogPostViewSet,        basename='blog')
router.register(r'faqs',                 FAQViewSet,             basename='faq')
router.register(r'partners',             PartnerViewSet,         basename='partner')
router.register(r'achievements',         AchievementViewSet,     basename='achievement')

urlpatterns = [
    # Singleton views (not in router)
    path('about/',    AboutPageView.as_view(),    name='about-page'),
    path('homepage/', HomepageDataView.as_view(), name='homepage-data'),

    # All ViewSet routes
    path('', include(router.urls)),
]
