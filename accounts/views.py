# accounts/views.py
from rest_framework import status, generics, permissions, serializers as s
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import secrets
from datetime import timedelta
from drf_spectacular.utils import extend_schema, inline_serializer
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, UpdateProfileSerializer,
    ChangePasswordSerializer, ResetPasswordEmailSerializer, ResetPasswordSerializer,
    UserProfileSerializer
)
from .models import UserProfile, PasswordResetToken


@extend_schema(
    responses={
        201: inline_serializer('RegisterResponse', {
            'message': s.CharField(),
            'user': UserSerializer(),
        })
    }
)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_mail(
            subject='Welcome to Interlink Global College',
            message=f"""
            Dear {user.first_name} {user.last_name},

            Thank you for registering with Interlink Global College!

            Your account has been successfully created. You can now login to access our courses and resources.

            Login credentials:
            Username: {user.username}
            Email: {user.email}

            Best regards,
            Interlink Global College Team
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )

        return Response({
            'message': 'Registration successful! Please login.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    request=LoginSerializer,
    responses={
        200: inline_serializer('LoginResponse', {
            'access': s.CharField(help_text='JWT access token'),
            'refresh': s.CharField(help_text='JWT refresh token'),
            'user': UserSerializer(),
        })
    }
)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(methods=['GET'], responses={200: UserSerializer})
@extend_schema(methods=['PUT'], request=UpdateProfileSerializer, responses={200: UserSerializer})
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UpdateProfileSerializer(
            request.user, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)


@extend_schema(
    request={'multipart/form-data': inline_serializer('ProfilePictureRequest', {
        'profile_picture': s.ImageField(),
    })},
    responses={
        200: inline_serializer('ProfilePictureResponse', {
            'message': s.CharField(),
            'profile_picture': s.URLField(allow_null=True),
        })
    }
)
class UpdateProfilePictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_profile = request.user.profile
        profile_picture = request.FILES.get('profile_picture')

        if not profile_picture:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.profile_picture = profile_picture
        user_profile.save()

        return Response({
            'message': 'Profile picture updated successfully',
            'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None
        })


@extend_schema(
    request=ChangePasswordSerializer,
    responses={200: inline_serializer('MessageResponse', {'message': s.CharField()})}
)
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password changed successfully'})


@extend_schema(
    request=ResetPasswordEmailSerializer,
    responses={200: inline_serializer('ResetRequestResponse', {'message': s.CharField()})}
)
class ResetPasswordRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=24)
        PasswordResetToken.objects.create(user=user, token=token, expires_at=expires_at)

        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        send_mail(
            subject='Password Reset Request - Interlink Global College',
            message=f"""
            Dear {user.get_full_name() or user.username},

            We received a request to reset your password for your Interlink Global College account.

            Click the link below to reset your password:
            {reset_link}

            This link will expire in 24 hours.

            If you didn't request this, please ignore this email.

            Best regards,
            Interlink Global College Team
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({'message': 'Password reset email sent successfully'})


@extend_schema(
    request=ResetPasswordSerializer,
    responses={200: inline_serializer('ResetConfirmResponse', {'message': s.CharField()})}
)
class ResetPasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Password reset successful. Please login with your new password.'})


@extend_schema(
    request=inline_serializer('LogoutRequest', {'refresh': s.CharField(help_text='JWT refresh token')}),
    responses={200: inline_serializer('LogoutResponse', {'message': s.CharField()})}
)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"message": "Successfully logged out"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(profile__role=role)
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    lookup_field = 'id'
