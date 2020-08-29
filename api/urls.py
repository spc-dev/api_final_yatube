from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, GroupList, FollowList


router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('posts/(?P<id>\d+)/comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('group/', GroupList.as_view(), name='group'),
    path('follow/', FollowList.as_view(), name='follow'),
    path('', include(router.urls)),
]
