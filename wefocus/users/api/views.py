from django.contrib.auth import get_user_model, login
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
import uuid
import hashlib

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["POST"])
    def anonymous(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            random_username = hashlib.md5(str(uuid.uuid4).encode('utf-8')).hexdigest()
            user = User.objects.create(username=random_username, is_temporary=True)
            serializer = UserSerializer(request.user, context={"request": request})
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return Response(status=status.HTTP_200_OK, data=serializer.data)
