from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = (
                "username",
                "email",
                "password"
                )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.pop('password', None)

        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError(('User not found'))

        user = User.objects.get(username=username)
        if user and user.is_active and user.check_password(password):
            self.refresh = self.get_token(user)
            validated_data['refresh'] = str(self.refresh)
            validated_data['access'] = str(self.refresh.access_token)
            return validated_data

        raise serializers.ValidationError("Email or password is incorrect")