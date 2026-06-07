from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactSubmitView, ContactMessageViewSet

router = DefaultRouter()
router.register(r'messages', ContactMessageViewSet, basename='contact-message')

urlpatterns = [
    path('submit/', ContactSubmitView.as_view(), name='contact-submit'),
    path('', include(router.urls)),
]
