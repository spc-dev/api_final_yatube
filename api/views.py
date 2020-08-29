from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets

from .models import Comment, Follow, Group, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post.objects, pk=self.kwargs['id'])
        queryset = Comment.objects.filter(post__id=post.id)
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post.objects, pk=self.kwargs['id'])
        serializer.save(author=self.request.user, post=post)


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowList(generics.ListCreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Follow.objects.all()
        username = self.request.query_params.get('search', None)
        if username is not None:
            queryset = queryset.filter(
                Q(user__username=username) |
                Q(following__username=username)
            )
        return queryset

    def perform_create(self, serializer):
        following = get_object_or_404(
            User,
            username=self.request.POST.get('following')
        )
        serializer.save(user=self.request.user, following=following)
