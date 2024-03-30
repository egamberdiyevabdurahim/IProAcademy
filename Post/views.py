from django.shortcuts import render
from django.db.models import Q, F, Count, Sum, Min, Max
from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, JSONParser

from .serializers import (CategorySer, PhotoSer, PostSer, PostGetSer, ViewerSer,
                          ViewerGetSer, LikeSer, LikeGetSer, CommentSer, CommentGetSer,
                          LikeCommentSer, LikeCommentGetSer, PhoneNameSer, ErrorsSer)
from .models import (Category, Photo, Post, Viewer, Like, Comment, LikeComment, PhoneName, Errors)
from User.serializers import UserSer
from User.models import User


class CategoryList(ListAPIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySer


class CategoryDetail(RetrieveAPIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySer


class PhotoList(ListAPIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    queryset = Photo.objects.all()
    serializer_class = PhotoSer


class PhotoDetail(RetrieveUpdateDestroyAPIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    queryset = Photo.objects.all()
    serializer_class = PhotoSer


# from jnius import autoclass
class ViewerList(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        viewer = Viewer.objects.all()

        # PythonActivity = autoclass('org.kivy.android.PythonActivity')
        # context = PythonActivity.mActivity

        # TelephonyManager = autoclass('android.telephony.TelephonyManager')
        # tm = context.getSystemService(context.TELEPHONY_SERVICE)

        # serial_number = tm.getDeviceId()
        # print(TelephonyManager)
        # print('--------------------------------')
        # print(serial_number)

        ser = ViewerGetSer(viewer, many=True)
        return Response(ser.data)
    
    def post(self, request):
        data=request.data
        ser = ViewerSer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)


class LikePost(APIView):
     parser_classes = [JSONParser, MultiPartParser]
     permission_classes = [AllowAny]
     # permission_classes = [IsAuthenticated]
     def get(self, request, id):
          post = Post.objects.filter(id=id).first()
          like = LikeComment.objects.filter(post=post)
          sum_likes = LikeComment.objects.filter(post=post).count()
          ser = LikeCommentGetSer(like, many=True)
          return Response({'data':ser.data,
                          'sum_likes':sum_likes})
     
     def post(self, request, id):
        post = Post.objects.filter(id=id).first()
        if Like.objects.filter(post=post):
             like = Like.objects.filter(post=post).first()
             if request.user in like.user.all():
                 like.user.remove(request.user)
                 return Response({'message': 'Deleted Successfully'})
             like.user.add(request.user)
             return Response({'message': 'Liked Successfully'})
        like = Like.objects.create(
            post=post
        )
        like.user.add(request.user)
        return Response({'message': 'Liked Successfully'})


class CommentPost(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    def get(self, request, id):
        post = Post.objects.filter(id=id).first()
        comment = Comment.objects.filter(post=post)
        sum_comments = Comment.objects.filter(post=post).count()
        ser = CommentGetSer(comment, many=True)
        return Response({'data':ser.data,
                         'sum_comments':sum_comments})
    
    def post(self, request, id):
        post = Post.objects.filter(id=id).first()
        data=request.data
        data['user'] = request.user
        data['post'] = post
        ser = CommentSer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)


class LikeCommentPost(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    def get(self, request, id):
         comment = Comment.objects.filter(id=id).first()
         like = LikeComment.objects.filter(comment=comment)
         sum_likes = LikeComment.objects.filter(comment=comment).count()
         ser = LikeCommentGetSer(like, many=True)
         return Response({'data':ser.data,
                          'sum_likes':sum_likes})

    def post(self, request, id):
        comment = Comment.objects.filter(id=id).first()
        if LikeComment.objects.filter(comment=comment):
             like = Like.objects.filter(comment=comment).first()
             if request.user in like.user.all():
                 like.user.remove(request.user)
                 return Response({'message': 'Deleted Successfully'})
             like.user.add(request.user)
             return Response({'message': 'Liked Successfully'})
        like = Like.objects.create(
            comment=comment
        )
        like.user.add(request.user)
        return Response({'message': 'Liked Successfully'})


class PostList(APIView):
     parser_classes = [JSONParser, MultiPartParser]
     permission_classes = [AllowAny]
     # permission_classes = [IsAuthenticated]
     def get(self, request):
        post = Post.objects.all()
        import subprocess

        def get_serial_number():
            try:
                output = subprocess.check_output(['getprop', 'ro.serialno'], universal_newlines=True)
                print(output)
                return output.strip()
            except subprocess.CalledProcessError:
                return 'Failed to get serial number'
        
        print(get_serial_number())
        ser = PostGetSer(post, many=True)
        return Response({'data':ser.data})
     
     def post(self, request):
        data=request.data
        ser = PostSer(data=data)
        if ser.is_valid():
            if request.data.get('photo'):
                news = ser.save()
                photo_list = request.data.getlist['photo', []]
                for x in photo_list:
                    p = Photo.objects.create(photo=x)
                    news.photo.add(p)
                return Response(ser.data)
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)


class PostDetail(APIView):
     parser_classes = [JSONParser, MultiPartParser]
     permission_classes = [AllowAny]
     # permission_classes = [IsAuthenticated]
     def get(self, request, id):
          post = Post.objects.filter(id=id).first()
          ser = PostGetSer(post, many=True)
          return Response({'data':ser.data})
     
     def patch(self, request, id):
        post = Post.objects.filter(id=id).first()
        data=request.data
        ser = PostSer(post, data=data, partial=True)
        if ser.is_valid():
            if request.data.get('photo'):
                news = ser.save()
                photo_list = request.data.getlist['photo', []]
                for x in photo_list:
                    p = Photo.objects.create(photo=x)
                    news.photo.add(p)
                return Response(ser.data)
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)


class PhoneNameList(APIView):
     parser_classes = [JSONParser, MultiPartParser]
     permission_classes = [AllowAny]
     # permission_classes = [IsAuthenticated]
     def get(self, request):
          phone_name = PhoneName.objects.all()
          ser = PhoneNameSer(phone_name, many=True)
          return Response({'data':ser.data})
     
     def post(self, request):
          data=request.data
          ser = PhoneNameSer(data=data)
          if ser.is_valid():
              ser.save()
              return Response(ser.data)
          return Response(ser.errors)


class PhoneNameDetail(APIView):
     parser_classes = [JSONParser, MultiPartParser]
     permission_classes = [AllowAny]
     # permission_classes = [IsAuthenticated]
     def get(self, request, id):
          phone_name = PhoneName.objects.filter(id=id).first()
          ser = PhoneNameSer(phone_name, many=True)
          return Response({'data':ser.data})
     
     def patch(self, request, id):
          phone_name = PhoneName.objects.filter(id=id).first()
          data=request.data
          ser = PhoneNameSer(phone_name, data=data, partial=True)
          if ser.is_valid():
              ser.save()
              return Response(ser.data)
          return Response(ser.errors)
     
     def delete(self, request, id):
          phone_name = PhoneName.objects.filter(id=id).first()
          phone_name.delete()
          return Response({'message': 'Deleted Successfully'})


class ErrorsList(APIView):
     parser_classes = [JSONParser, MultiPartParser]
     permission_classes = [AllowAny]
     # permission_classes = [IsAuthenticated]
     def get(self, request):
          error = Errors.objects.all()
          ser = ErrorsSer(error, many=True)
          return Response({'data':ser.data})
     
     def post(self, request):
          data=request.data
          ser = ErrorsSer(data=data)
          if ser.is_valid():
              ser.save()
              return Response(ser.data)
          return Response(ser.errors)


class ErrorsDetail(APIView):
     parser_classes = [JSONParser, MultiPartParser]
     permission_classes = [AllowAny]
     # permission_classes = [IsAuthenticated]
     def get(self, request, id):
          error = Errors.objects.filter(id=id).first()
          ser = ErrorsSer(error, many=True)
          return Response({'data':ser.data})
     
     def patch(self, request, id):
          error = Errors.objects.filter(id=id).first()
          data=request.data
          ser = ErrorsSer(error, data=data, partial=True)
          if ser.is_valid():
              ser.save()
              return Response(ser.data)
          return Response(ser.errors)
     
     def delete(self, request, id):
          error = Errors.objects.filter(id=id).first()
          error.delete()
          return Response({'message': 'Deleted Successfully'})
