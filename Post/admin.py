from django.contrib import admin

from .models import Category, Photo, Post, Viewer, Like, Comment, LikeComment, PhoneName, Errors


admin.site.register(Category)

admin.site.register(Photo)

admin.site.register(Post)

admin.site.register(Viewer)

admin.site.register(Like)

admin.site.register(Comment)

admin.site.register(LikeComment)

admin.site.register(PhoneName)

admin.site.register(Errors)