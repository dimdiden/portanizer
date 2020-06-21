from rest_framework import serializers
from .models import Post


class PostsSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = ('user', 'title', 'body', 'tag')
