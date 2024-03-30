from django.urls import path

from .views import ForgotPasswordView, ChangePasswordView, Userdetail, SignUp


urlpatterns = [
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('userdetail/<int:id>/', Userdetail.as_view(), name='userdetail'),
    path('signup/', SignUp.as_view(), name='signup'),
]