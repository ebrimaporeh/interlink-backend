# resources/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResourceCategoryViewSet, ResourceViewSet,
    ResourceCollectionViewSet, StudyGuideViewSet, UserBookmarkViewSet,
    PopularTagsView, ResourceStatsView, ResourceSearchView, TrendingResourcesView,
)

router = DefaultRouter()
router.register(r'categories',   ResourceCategoryViewSet,   basename='resource-category')
router.register(r'collections',  ResourceCollectionViewSet, basename='resource-collection')
router.register(r'study-guides', StudyGuideViewSet,         basename='study-guide')
router.register(r'bookmarks',    UserBookmarkViewSet,        basename='bookmark')
# Register resources last — broad lookup regex ([\w-]+) must not shadow fixed paths
router.register(r'', ResourceViewSet, basename='resource')

urlpatterns = [
    # Fixed-path views — matched BEFORE router.urls
    path('stats/',        ResourceStatsView.as_view(),     name='resource-stats'),
    path('search/',       ResourceSearchView.as_view(),    name='resource-search'),
    path('trending/',     TrendingResourcesView.as_view(), name='trending-resources'),
    path('tags/popular/', PopularTagsView.as_view(),       name='popular-tags'),

    # All ViewSet routes
    path('', include(router.urls)),
]