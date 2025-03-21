from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from projects.models import Project
from projects.permissions import IsProjectAdmin, IsProjectStaffAndReadOnly
from projects.serializers import ProjectPolymorphicSerializer

from projects.models import Perspective
from projects.serializers import PerspectiveSerializer

from rest_framework.views import APIView

class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectPolymorphicSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "description")
    ordering_fields = ["name", "created_at", "created_by", "project_type"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                IsAuthenticated,
            ]
        else:
            self.permission_classes = [IsAuthenticated & IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        return Project.objects.filter(role_mappings__user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        project.add_admin()

    def delete(self, request, *args, **kwargs):
        delete_ids = request.data["ids"]
        projects = Project.objects.filter(
            role_mappings__user=self.request.user,
            role_mappings__role__name=settings.ROLE_PROJECT_ADMIN,
            pk__in=delete_ids,
        )
        for project in projects:
            project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectPolymorphicSerializer
    lookup_url_kwarg = "project_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]


class CloneProject(views.APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        cloned_project = project.clone()
        serializer = ProjectPolymorphicSerializer(cloned_project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class PerspectiveViewSet(viewsets.ModelViewSet):
    serializer_class = PerspectiveSerializer

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return Perspective.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_id")
        project = get_object_or_404(Project, id=project_id)
        serializer.context['project'] = project
        serializer.save(project=project)