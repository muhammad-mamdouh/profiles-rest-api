from django.urls            import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    HelloApiView,
    HelloViewSet,
    UserProfileViewSet,
    UserLoginApiView,
    UserProfileFeedViewSet,
)


router = DefaultRouter()
router.register('hello-viewset', HelloViewSet, base_name='Hello-viewset')
router.register('profile', UserProfileViewSet)     # we don't need to specify a base_name because in our ViewSet we have a queryset object
router.register('feed', UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', HelloApiView.as_view(), name='hello-view'),
    path('login/', UserLoginApiView.as_view(), name='user-profile-login'),
    path('', include(router.urls)),
]
