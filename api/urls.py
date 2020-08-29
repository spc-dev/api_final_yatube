from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowList, GroupList, PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('posts/(?P<id>\d+)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/group/', GroupList.as_view(), name='group'),
    path('v1/follow/', FollowList.as_view(), name='follow'),
    path('v1/', include(router.urls)),
]
