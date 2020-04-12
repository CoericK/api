from django.contrib.auth import get_user_model, login
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils.crypto import get_random_string

from .serializers import UserSerializer
from rest_framework.authtoken.models import Token

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
        print(request.user)
        if request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            random_username = get_random_string(length=32)
            user = User.objects.create(username=random_username, is_temporary=True)
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            serializer = UserSerializer(request.user, context={"request": request})
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'key': token.key,
            }, status=status.HTTP_201_CREATED)
