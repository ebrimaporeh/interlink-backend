# resources/views.py
from rest_framework import viewsets, permissions, filters, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum
from django.http import FileResponse
from django.utils import timezone
from datetime import timedelta
from taggit.models import Tag
from .models import (
    ResourceCategory, Resource, ResourceRating, ResourceDownload,
    ResourceCollection, UserBookmark, StudyGuide, ResourceView,
    ResourceSearchHistory
)
from .serializers import (
    ResourceCategorySerializer, ResourceListSerializer, ResourceDetailSerializer,
    ResourceRatingSerializer, ResourceCollectionSerializer, UserBookmarkSerializer,
    StudyGuideSerializer, TagSerializer, ResourceStatsSerializer
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


def _get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0] if xff else request.META.get('REMOTE_ADDR')


# ── Resource Categories ───────────────────────────────────────────────────────
class ResourceCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name']

    def get_queryset(self):
        if _is_admin(self.request):
            return ResourceCategory.objects.all()
        return ResourceCategory.objects.filter(is_active=True)


# ── Resources ─────────────────────────────────────────────────────────────────
class ResourceViewSet(viewsets.ModelViewSet):
    """
    Supports both slug (public) and integer PK (admin) in the URL.
    Custom actions: download, rate, like.
    """
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = MULTIPART
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'file_type', 'difficulty_level', 'is_featured']
    search_fields = ['title', 'description', 'short_description', 'author', 'tags__name']
    ordering_fields = ['-downloads', '-views', '-published_date', 'title']
    lookup_field = 'pk'
    lookup_value_regex = r'[\w-]+'

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update', 'partial_update'):
            return ResourceDetailSerializer
        return ResourceListSerializer

    def get_queryset(self):
        qs = Resource.objects.all() if _is_admin(self.request) else Resource.objects.filter(is_active=True)
        if not _is_admin(self.request):
            for param, field in [('category', 'category__slug'), ('file_type', 'file_type'),
                                  ('difficulty', 'difficulty_level')]:
                val = self.request.query_params.get(param)
                if val:
                    qs = qs.filter(**{field: val})
            tag = self.request.query_params.get('tag')
            if tag:
                qs = qs.filter(tags__name__iexact=tag)
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

    def perform_create(self, serializer):
        user = self.request.user
        author_name = user.get_full_name().strip() or user.username
        serializer.save(author=author_name)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        ResourceView.objects.create(
            resource=instance,
            user=request.user if request.user.is_authenticated else None,
            ip_address=_get_client_ip(request),
        )
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def download(self, request, pk=None):
        resource = self.get_object()
        if resource.requires_login and not request.user.is_authenticated:
            return Response({'error': 'Login required to download.'}, status=status.HTTP_401_UNAUTHORIZED)
        resource.downloads += 1
        resource.save(update_fields=['downloads'])
        ResourceDownload.objects.create(
            resource=resource,
            user=request.user if request.user.is_authenticated else None,
            ip_address=_get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )
        if resource.file and resource.file.name:
            try:
                return FileResponse(resource.file.open(), as_attachment=True,
                                    filename=resource.file.name.split('/')[-1])
            except Exception:
                pass
        if resource.file_url:
            return Response({'download_url': resource.file_url})
        return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def rate(self, request, pk=None):
        resource = self.get_object()
        serializer = ResourceRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(resource=resource)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        resource = self.get_object()
        resource.likes += 1
        resource.save(update_fields=['likes'])
        return Response({'likes': resource.likes})


# ── Resource Collections ──────────────────────────────────────────────────────
class ResourceCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceCollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title']
    lookup_field = 'slug'

    def get_queryset(self):
        if _is_admin(self.request):
            return ResourceCollection.objects.all()
        return ResourceCollection.objects.filter(is_active=True)


# ── Study Guides ──────────────────────────────────────────────────────────────
class StudyGuideViewSet(viewsets.ModelViewSet):
    serializer_class = StudyGuideSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title']
    lookup_field = 'slug'

    def get_queryset(self):
        if _is_admin(self.request):
            return StudyGuide.objects.all()
        return StudyGuide.objects.filter(is_active=True)


# ── User Bookmarks ────────────────────────────────────────────────────────────
class UserBookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = UserBookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        return UserBookmark.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # Allow deletion by resource_id as well as bookmark pk
        resource_id = kwargs.get('pk')
        bookmark = UserBookmark.objects.filter(
            user=request.user, resource_id=resource_id
        ).first() or UserBookmark.objects.filter(user=request.user, pk=resource_id).first()
        if bookmark:
            bookmark.delete()
            return Response({'message': 'Bookmark removed.'})
        return Response({'error': 'Bookmark not found.'}, status=status.HTTP_404_NOT_FOUND)


# ── Popular Tags ──────────────────────────────────────────────────────────────
class PopularTagsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        tags = Tag.objects.filter(
            taggit_taggeditem_items__isnull=False
        ).distinct().annotate(
            num_resources=Count('taggit_taggeditem_items')
        ).order_by('-num_resources')[:20]
        return Response(TagSerializer(tags, many=True).data)


# ── Resource Stats ────────────────────────────────────────────────────────────
class ResourceStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        total_resources = Resource.objects.filter(is_active=True).count()
        total_downloads = Resource.objects.filter(is_active=True).aggregate(Sum('downloads'))['downloads__sum'] or 0
        total_views     = Resource.objects.filter(is_active=True).aggregate(Sum('views'))['views__sum'] or 0
        top_categories  = ResourceCategory.objects.filter(resources__is_active=True).annotate(
            resource_count=Count('resources')
        ).order_by('-resource_count')[:5].values('name', 'resource_count')
        popular_tags = Tag.objects.filter(
            taggit_taggeditem_items__isnull=False
        ).annotate(count=Count('taggit_taggeditem_items')).order_by('-count')[:10].values('name', 'count')

        return Response({
            'total_resources': total_resources,
            'total_downloads': total_downloads,
            'total_views':     total_views,
            'top_categories':  list(top_categories),
            'popular_tags':    list(popular_tags),
        })


# ── Resource Search ───────────────────────────────────────────────────────────
class ResourceSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        if query and request.user.is_authenticated:
            ResourceSearchHistory.objects.create(user=request.user, query=query, results_count=0)
        qs = Resource.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) |
            Q(author__icontains=query) | Q(tags__name__icontains=query),
            is_active=True,
        ).distinct()
        return Response(ResourceListSerializer(qs, many=True, context={'request': request}).data)


# ── Trending Resources ────────────────────────────────────────────────────────
class TrendingResourcesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        qs = Resource.objects.filter(
            is_active=True,
            download_records__downloaded_at__gte=thirty_days_ago,
        ).annotate(recent_downloads=Count('download_records')).order_by('-recent_downloads')[:10]
        return Response(ResourceListSerializer(qs, many=True, context={'request': request}).data)
