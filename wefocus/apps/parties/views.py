from django.contrib.auth import get_user_model
from rest_framework import decorators, permissions, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from wefocus.apps.parties.models import Party
from .serializers import PartySerializer
from .api import PartyManger

import logging

User = get_user_model()


def handle_response(response, **kwargs):
    try:
        return response(**kwargs)
    except Exception as e:
        logging.exception('handle_response - e: %s' % str(e))
        return Response(status=e.status_code if getattr(e, 'status_code', None) else status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'message': str(e)})


class PartyViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PartySerializer
    queryset = Party.objects.all()
    lookup_field = "slug"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.data.get("slug"))

    def create(self, request):
        return handle_response(PartyManger().create_party,
                               host_user_id=request.user.id,
                               )

    def retrieve(self, request, *args, **kwargs):
        return handle_response(PartyManger().get_party_view,
                               user_id=request.user.id,
                               party_slug=kwargs.get('slug'),
                               )

    @action(detail=False, methods=["GET"])
    def get_parties(self, request):
        return handle_response(PartyManger().get_parties)

    @action(detail=False, methods=["POST"])
    def join_party(self, request):
        return handle_response(PartyManger().join_party,
                               user_id=request.user.id,
                               party_slug=request.data.get('slug'),
                               )

    # INTERNAL USE. do not expose when we are done.
    @action(detail=False, methods=["POST"])
    def delete_party(self, request):
        return handle_response(PartyManger().delete_party,
                               party_slug=request.data.get('slug'),
                               )

    @action(detail=False, methods=["POST"])
    def leave_party(self, request):
        return handle_response(PartyManger().leave_party,
                               user_id=request.user.id,
                               party_slug=request.data.get('slug'),
                               )

    @action(detail=False, methods=["POST"])
    def start_pomodoro_timer(self, request):
        return handle_response(PartyManger().start_pomodoro_timer,
                               user_id=request.user.id,
                               party_slug=request.data.get('slug'),
                               focus_duration=request.data.get('focus_duration'),
                               break_duration=request.data.get('break_duration'),
                               )

    @action(detail=False, methods=["POST"])
    def restart_pomodoro_timer(self, request):
        return handle_response(PartyManger().restart_pomodoro_timer,
                               user_id=request.user.id,
                               party_slug=request.data.get('slug'),
                               focus_duration=request.data.get('focus_duration'),
                               break_duration=request.data.get('break_duration'),
                               )

    @action(detail=False, methods=["POST"])
    def end_pomodoro_timer(self, request):
        return handle_response(PartyManger().end_pomodoro_timer,
                               user_id=request.user.id,
                               party_slug=request.data.get('slug'),
                               )
