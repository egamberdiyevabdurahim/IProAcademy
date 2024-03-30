from django.urls import path

from .views import (CategoryList, CategoryDetail, PhotoDetail, ViewerList,
                    LikePost, CommentPost, LikeCommentPost, PostList, PostDetail,
                    PhoneNameList, PhoneNameDetail, ErrorsList, ErrorsDetail)


urlpatterns = [
    path('category/', CategoryList.as_view()),
    path('category/<int:id>/', CategoryDetail.as_view()),
    path('phone-name/', PhoneNameList.as_view()),
    path('phone-name/<int:id>/', PhoneNameDetail.as_view()),
    path('photo/', PhotoDetail.as_view()),
    path('photo/<int:id>/', PhotoDetail.as_view()),
    path('post/', PostList.as_view()),
    path('post/<int:id>/', PostDetail.as_view()),
    path('viewer/', ViewerList.as_view()),
    path('like-post/<int:id>/', LikePost.as_view()),
    path('comment-post/<int:id>/', CommentPost.as_view()),
    path('like-comment-post/<int:id>/', LikeCommentPost.as_view()),
    path('errors/', ErrorsList.as_view()),
    path('errors/<int:id>/', ErrorsDetail.as_view()),
]