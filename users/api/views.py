from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer, ChangePasswordSerializer
from .permissions import IsAdminOrJury, IsAdminOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response({"error": "You cannot deactivate yourself."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = False  # Soft delete
        user.save()
        return Response({"detail": "User deactivated."}, status=status.HTTP_204_NO_CONTENT)

    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminOnly])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            new_password = serializer.validated_data["new_password"]
            
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            # Change the user's password
            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password changed successfully."})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
'''
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
'''

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            
            if not user.is_active:
                return Response({"error": "Your account has been deactivated."}, status=status.HTTP_403_FORBIDDEN)

            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

