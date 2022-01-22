from rest_framework.routers import SimpleRouter

from users.views import UserProfileViewSet


router = SimpleRouter()
router.register('users', UserProfileViewSet, basename='users')

urlpatterns = [

]

urlpatterns += router.urls
