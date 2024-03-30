from django.shortcuts import render
from django.db.models import Q, F, Sum, Min, Max
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone

from genericpath import exists

from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
# from Post.models import *
from .serializers import UserSer, ChangePasswordSerializer, ForgotPasswordSerializer


class ForgotPasswordView(APIView):
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if request.user.is_authenticated and request.user.status == 'Admin':
            if serializer.is_valid():
                username = serializer.data.get("username")
                new_password = serializer.data.get("new_password")
                user = get_user_model().objects.filter(username=username).first()
                if user:
                    user.set_password(new_password)
                    user.save()
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return Response({
                    "detail": "Password updated successfully",
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)
                return Response({'message': 'User topilmadi'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Siz admin emassiz yoki ro\'yxatdan o\'tmagansiz'})



class ChangePasswordView(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = self.request.user
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'})

            user.set_password(new_password)
            user.save()
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({'detail': 'Password changed successfully.',
                             'access_token': access,
                             'refresh_token': str(refresh)
                             })

        return Response(serializer.errors)


class Userdetail(APIView):
    # permission_classes = [IsAuthenticated,] 
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            ser = UserSer(user)
            return Response(ser.data)
        except:
            return Response({'message': 'bu id xato'})
    
    def patch(self, request, id):
        user = User.objects.filter(id=id).first()
        ser = UserSer(data=request.data, instance=user, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        if request.user.status=='Admin':
            user.delete()
            return Response(status=204)


class SignUp(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        user = User.objects.all()
        ser = UserSer(user, many=True)
        return Response(ser.data)

    def post(self, request):
        data = request.data
        ser = UserSer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)