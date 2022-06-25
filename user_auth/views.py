from user_auth.serializers import UserLoginSerializer, UserRegisterSerializer

from rest_framework import response, status, views
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegisterView(views.APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)

class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)