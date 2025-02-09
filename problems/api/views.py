from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Problem
from .serializers import AdminProblemSerializer, UserProblemSerializer

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):    
        return request.user.is_authenticated and request.user.is_admin()

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    
    def get_serializer_class(self):
        if self.request.user.is_admin():
            return AdminProblemSerializer
        return UserProblemSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.is_admin():
            return Response({'detail': 'Permission Denied'}, status=403)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_admin():
            return Response({'detail': 'Permission Denied'}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_admin():
            return Response({'detail': 'Permission Denied'}, status=403)
        return super().destroy(request, *args, **kwargs)
