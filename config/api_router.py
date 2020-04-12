from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from wefocus.users.api.views import UserViewSet
from wefocus.apps.parties.views import PartyViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register('parties', PartyViewSet)


app_name = "api"
urlpatterns = router.urls
