from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import pagination
from rest_framework import generics
from taggit.models import Tag
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import filters

from core import serializers
from .models import Post


class PageNumberSetPagination(pagination.PageNumberPagination):
    """
    Класс реализации пагинации на страницах.
    """
    page_size = 2  # количество постов на одной странице
    page_size_query_param = 'page_size'  # указывает на имя параметра, с помощбю которого пользователь может управлять
                                         # количеством постов на одной странице
    ordering = 'created_at'  # поле, по которому происходит сортировка


class PostViewSet(viewsets.ModelViewSet):
    """
    Класс отображения записей блога.
    """
    search_fields = ['content', 'h1']  # поиск по перечисленным полям
    filter_backends = (filters.SearchFilter, )  # вид фильтра, который будет осуществлять поиск

    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'  # поле по которому получают одну конкретную запись
    permission_classes = [permissions.AllowAny]  # доступ к постам может получить каждый, вне зависмости от авторизации
    pagination_class = PageNumberSetPagination


class TagDetailView(generics.ListAPIView):
    """
    Класс получения постов по тегам.
    """
    serializer_class = serializers.PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class TagView(generics.ListAPIView):
    """
    Класс представления для сериализатора тегов.
    """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    """
    Класс предтсавления, возвращает 2 последние записи (post).
    """
    queryset = Post.objects.all().order_by('-id')[:2]
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    """
    Класс представения для формы обратной связи.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ContanctSerializer

    def post(self, request, *args, **kwargs):
        """
        Метод отправки формы обратной связи
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_class = serializers.ContanctSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['amromashov@gmail.com'])
            return Response({"success": "Sent"})


class RegisterView(generics.GenericAPIView):
    """
    Класс представления регистрации пользователей.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Метод отправки и сохранения данных пользоватедя.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': serializers.UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Пользователь успешно создан',
        })


class ProfileView(generics.GenericAPIView):
    """
    Класс представления для отображения профиля пользователя.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        """
        Метод получения данных о пользователе.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return Response({
            'user': serializers.UserSerializer(request.user, context=self.get_serializer_context()).data,
        })
