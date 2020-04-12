from django.contrib.auth import get_user_model
from rest_framework import decorators, permissions, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from wefocus.apps.parties.models import Party
from .serializers import PartySerializer
from .api import PartyManger

User = get_user_model()


def handle_response(response, **kwargs):
    try:
        return response(**kwargs)
    except Exception as e:
        return Response(status=e.status_code if getattr(e, 'status_code') else status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'message': str(e)})


class PartyViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = PartySerializer
    queryset = Party.objects.all()
    lookup_field = "slug"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.data.get("slug"))

    @permission_classes([permissions.IsAuthenticated])
    def create(self, request):
        return handle_response(PartyManger().create_party, host_user_id=request.user.id)

    @action(detail=False, methods=["GET"])
    @permission_classes([permissions.IsAuthenticated])
    def get_parties(self, request):
        return handle_response(PartyManger().get_parties)

    @action(detail=False, methods=["POST"])
    @permission_classes([permissions.IsAuthenticated])
    def delete_party(self, request):
        return handle_response(PartyManger().delete_party, party_slug=request.data['party_slug'])
