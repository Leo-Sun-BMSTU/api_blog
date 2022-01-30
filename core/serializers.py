from rest_framework import serializers
from .models import Post
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """
    Класс перевода данных поста в формат JSON.
    """
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        """

        """
        model = Post
        fields = ("id", "h1", "title", "slug", "description", "content", "image", "created_at", "author", "tags")
        lookup_fields = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug', },
        }


class TagSerializer(serializers.ModelSerializer):
    """
    Класс перевода данных тэегов в формат JSON.
    """
    class Meta:
        model = Tag
        fields = ('name',)
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'},
        }


class ContanctSerializer(serializers.Serializer):
    """
    Класс сериалайзер для формы обратной связи.
    """
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Класс сериалайзер для регистрации.
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        """
        Создаёт сериалайзер на основе модели пользователя.
        """
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Метод для создания и сохранения пользователей.
        :param validated_data:
        :return:
        """
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Класс сериалайзера, возвращающий все данные о пользователе.
    """
    class Meta:
        model = User
        fields = '__all__'
