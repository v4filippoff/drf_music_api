from rest_framework.routers import SimpleRouter

from users.views import UserProfileViewSet


router = SimpleRouter()
router.register('users', UserProfileViewSet)

urlpatterns = [

]

urlpatterns += router.urls
