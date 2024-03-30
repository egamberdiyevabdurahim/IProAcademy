from django.db import models

from User.models import User


class Category(models.Model):
    STATUS = (
        ('Android', 'Android'),
        ('Apple', 'Apple'),
    )
    name = models.CharField(max_length=30, choices=STATUS, default='Android')

    def __str__(self):
        return self.name


class PhoneName(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Errors(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Photo(models.Model):
    photo = models.ImageField(upload_to='post_photo')

    def __str__(self):
        return self.photo.name


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='post_category')
    
    errors = models.ManyToManyField(Errors, related_name='post_errors')
    photo = models.ManyToManyField(Photo, related_name='post_photo')
    video = models.FileField(upload_to='post_video', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='news_user')

    @property
    def sum_of_viewer(self):
        return self.viewer_post.user.count()

    @property
    def sum_of_like(self):
        return self.like_post.user.count()

    def __str__(self):
        return f'{self.title}/{self.category.name}'


class Viewer(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='viewer_post')
    user = models.ManyToManyField(User, related_name='viwer_user')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.title}/{self.user.first_name}'


class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='like_post')
    user = models.ManyToManyField(User, related_name='like_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post.title}/{self.user.first_name}'


class Comment(models.Model):
    comment = models.TextField(verbose_name='Izoh')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')

    @property
    def sum_of_likecom(self):
        return self.likecomment_comment.user.count()
    
    def __str__(self):
        return f'{self.comment.comment}/{self.user.first_name}'


class LikeComment(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='likecomment_comment')
    user = models.ManyToManyField(User, related_name='likecomment_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.comment.comment}/{self.user.first_name}'
