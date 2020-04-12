from django.contrib.auth import get_user_model
from rest_framework import decorators, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet


from wefocus.apps.parties.models import Party
from .serializers import PartySerializer
from .api import PartyManger

User = get_user_model()


class PartyViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = PartySerializer
    queryset = Party.objects.all()
    lookup_field = "slug"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.data.get("slug"))

    @permission_classes([permissions.IsAuthenticated])
    def create(self, request):
        return PartyManger().create_party(host_user_id=request.user.id)
