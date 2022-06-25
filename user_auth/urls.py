from django.urls import path

from user_auth.views import UserRegisterView, UserLoginView

urlpatterns = [
    path('signup/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view())
]