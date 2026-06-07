# content/views.py
from rest_framework import viewsets, permissions, filters, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import (
    AboutPage, TeamMember, GalleryCategory, GalleryItem,
    PolicyCategory, Policy, Testimonial, BlogCategory,
    BlogPost, FAQ, Partner, Achievement, HomepageSettings
)
from .serializers import (
    AboutPageSerializer, TeamMemberSerializer, GalleryCategorySerializer,
    GalleryItemSerializer, PolicyCategorySerializer, PolicySerializer,
    TestimonialSerializer, BlogCategorySerializer, BlogPostListSerializer,
    BlogPostDetailSerializer, FAQSerializer, PartnerSerializer, AchievementSerializer
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


# ── About Page (singleton) ────────────────────────────────────────────────────
class AboutPageView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = MULTIPART

    def _get_object(self):
        obj, _ = AboutPage.objects.get_or_create(id=1)
        return obj

    def get(self, request):
        return Response(AboutPageSerializer(self._get_object(), context={'request': request}).data)

    def put(self, request):
        serializer = AboutPageSerializer(self._get_object(), data=request.data, partial=False, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        serializer = AboutPageSerializer(self._get_object(), data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ── Team Members ──────────────────────────────────────────────────────────────
class TeamMemberViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = MULTIPART
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'position', 'expertise']
    ordering_fields = ['order', 'name']

    def get_queryset(self):
        if _is_admin(self.request):
            return TeamMember.objects.all()
        return TeamMember.objects.filter(is_active=True)


# ── Gallery ───────────────────────────────────────────────────────────────────
class GalleryCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = GalleryCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']

    def get_queryset(self):
        if _is_admin(self.request):
            return GalleryCategory.objects.all()
        return GalleryCategory.objects.filter(is_active=True)


class GalleryItemViewSet(viewsets.ModelViewSet):
    serializer_class = GalleryItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = MULTIPART
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'media_type', 'is_featured']
    search_fields = ['title', 'caption', 'description']
    ordering_fields = ['order', '-created_at', 'views']

    def get_queryset(self):
        qs = GalleryItem.objects.all() if _is_admin(self.request) else GalleryItem.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        media_type = self.request.query_params.get('media_type')
        if media_type:
            qs = qs.filter(media_type=media_type)
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        item = self.get_object()
        item.likes += 1
        item.save(update_fields=['likes'])
        return Response({'likes': item.likes})


# ── Policies ──────────────────────────────────────────────────────────────────
class PolicyCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = PolicyCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']

    def get_queryset(self):
        if _is_admin(self.request):
            return PolicyCategory.objects.all()
        return PolicyCategory.objects.filter(is_active=True)


class PolicyViewSet(viewsets.ModelViewSet):
    serializer_class = PolicySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__slug', 'category__id']
    search_fields = ['title', 'content']

    def get_queryset(self):
        qs = Policy.objects.all() if _is_admin(self.request) else Policy.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs


# ── Testimonials ──────────────────────────────────────────────────────────────
class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = MULTIPART
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', '-created_at', 'rating']

    def get_queryset(self):
        qs = Testimonial.objects.all() if _is_admin(self.request) else Testimonial.objects.filter(is_active=True)
        if self.request.query_params.get('featured') == 'true':
            qs = qs.filter(is_featured=True)
        return qs


# ── Blog ──────────────────────────────────────────────────────────────────────
class BlogCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if _is_admin(self.request):
            return BlogCategory.objects.all()
        return BlogCategory.objects.filter(is_active=True)


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    Supports both integer PK (admin CRUD) and slug (public read) in the same URL.
    GET  /blog/my-post-slug/   → public detail by slug
    GET  /blog/6/              → detail by pk
    PATCH /blog/6/             → admin update by pk
    DELETE /blog/6/            → admin delete by pk
    """
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = MULTIPART
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'is_featured']
    search_fields = ['title', 'excerpt', 'content', 'author', 'tags']
    ordering_fields = ['-published_at', '-views', '-likes']
    # Allow both integer IDs and slugs in the URL
    lookup_field = 'pk'
    lookup_value_regex = r'[\w-]+'

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update', 'partial_update'):
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def get_queryset(self):
        qs = BlogPost.objects.all() if _is_admin(self.request) else BlogPost.objects.filter(is_published=True)
        if not _is_admin(self.request):
            category = self.request.query_params.get('category')
            if category:
                qs = qs.filter(category__slug=category)
            tag = self.request.query_params.get('tag')
            if tag:
                qs = qs.filter(tags__icontains=tag)
            search = self.request.query_params.get('search')
            if search:
                qs = qs.filter(
                    Q(title__icontains=search) | Q(content__icontains=search) | Q(tags__icontains=search)
                )
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
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes += 1
        post.save(update_fields=['likes'])
        return Response({'likes': post.likes})

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        post = self.get_object()
        related = BlogPost.objects.filter(
            is_published=True, category=post.category
        ).exclude(pk=post.pk)[:3]
        return Response(BlogPostListSerializer(related, many=True, context={'request': request}).data)


# ── FAQs ─────────────────────────────────────────────────────────────────────
class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'category']

    def get_queryset(self):
        qs = FAQ.objects.all() if _is_admin(self.request) else FAQ.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs


# ── Partners ──────────────────────────────────────────────────────────────────
class PartnerViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = MULTIPART
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']

    def get_queryset(self):
        if _is_admin(self.request):
            return Partner.objects.all()
        return Partner.objects.filter(is_active=True)


# ── Achievements ──────────────────────────────────────────────────────────────
class AchievementViewSet(viewsets.ModelViewSet):
    serializer_class = AchievementSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['-year', 'order']

    def get_queryset(self):
        if _is_admin(self.request):
            return Achievement.objects.all()
        return Achievement.objects.filter(is_active=True)


# ── Homepage (singleton aggregation + admin settings) ─────────────────────────
class HomepageDataView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        settings = HomepageSettings.objects.first()

        if not settings or not settings.is_active:
            featured_testimonials = Testimonial.objects.filter(is_featured=True, is_active=True)[:3]
            featured_gallery      = GalleryItem.objects.filter(is_featured=True, is_active=True)[:8]
            recent_blog_posts     = BlogPost.objects.filter(is_published=True)[:3]
            team_members          = TeamMember.objects.filter(is_active=True)[:4]
            partners              = Partner.objects.filter(is_active=True)[:6]
            about = AboutPage.objects.first()
            stats = about.stats if about else []
        else:
            featured_testimonials = settings.featured_testimonials.filter(is_active=True)[:settings.max_testimonials]
            featured_gallery      = settings.featured_gallery.filter(is_active=True)[:settings.max_gallery_items]
            recent_blog_posts     = settings.featured_blog_posts.filter(is_published=True)[:settings.max_blog_posts]
            team_members          = settings.featured_team_members.filter(is_active=True)[:settings.max_team_members]
            partners              = settings.featured_partners.filter(is_active=True)[:settings.max_partners]
            stats = settings.stats if settings.stats else []

        ctx = {'request': request}
        return Response({
            'hero': {
                'title':      settings.title if settings else "Welcome to Interlink Global College",
                'subtitle':   settings.subtitle if settings else "",
                'hero_image': settings.hero_image.url if settings and settings.hero_image else None,
            },
            'stats': stats,
            'featured_testimonials': TestimonialSerializer(featured_testimonials, many=True, context=ctx).data,
            'featured_gallery':      GalleryItemSerializer(featured_gallery, many=True, context=ctx).data,
            'recent_blog_posts':     BlogPostListSerializer(recent_blog_posts, many=True, context=ctx).data,
            'team_members':          TeamMemberSerializer(team_members, many=True, context=ctx).data,
            'partners':              PartnerSerializer(partners, many=True, context=ctx).data,
        })

    def patch(self, request):
        if not _is_admin(request):
            return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)
        settings_obj, _ = HomepageSettings.objects.get_or_create(id=1)
        for field in ['title', 'subtitle', 'is_active', 'stats',
                      'max_testimonials', 'max_gallery_items',
                      'max_blog_posts', 'max_team_members', 'max_partners']:
            if field in request.data:
                setattr(settings_obj, field, request.data[field])
        if 'hero_image' in request.FILES:
            settings_obj.hero_image = request.FILES['hero_image']
        settings_obj.save()
        return Response({'status': 'updated'})
