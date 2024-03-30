from rest_framework import serializers

from .models import Category, Photo, Post, Viewer, Like, Comment, LikeComment, PhoneName, Errors
from User.serializers import UserSer


class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PhoneNameSer(serializers.ModelSerializer):
    class Meta:
        model = PhoneName
        fields = '__all__'


class ErrorsSer(serializers.ModelSerializer):
    class Meta:
        model = Errors
        fields = '__all__'


class PhotoSer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class PostSer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('photo')
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        # instance.photo = validated_data.get('photo', instance.photo)
        instance.category = validated_data.get('category', instance.category)
        # instance.tag = validated_data.get('tag', instance.tag)
        instance.video = validated_data.get('video', instance.video)
        instance.save()
        return instance


class PostGetSer(serializers.ModelSerializer):
    user = UserSer()
    photo = PhotoSer()
    category = CategorySer(many=True)
    # tag = PhoneNameSer()
    errors = ErrorsSer()
    class Meta:
        model = Post
        fields = '__all__'


class ViewerSer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
        fields = '__all__'


class ViewerGetSer(serializers.ModelSerializer):
    user = UserSer()
    post = PostSer()
    class Meta:
        model = Viewer
        fields = '__all__'


class LikeSer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class LikeGetSer(serializers.ModelSerializer):
    user = UserSer()
    post = PostSer()
    class Meta:
        model = Like
        fields = '__all__'


class CommentSer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentGetSer(serializers.ModelSerializer):
    user = UserSer()
    post = PostSer()
    class Meta:
        model = Comment
        fields = '__all__'


class LikeCommentSer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'


class LikeCommentGetSer(serializers.ModelSerializer):
    user = UserSer()
    comment = CommentSer()
    class Meta:
        model = LikeComment
        fields = '__all__'