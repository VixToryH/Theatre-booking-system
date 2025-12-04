from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
    write_only=True,
    min_length=8,
    error_messages = {
        "min_length": "Пароль має містити щонайменше 8 символів."
    }

)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def validate_email(self, value):
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError(
                "Email повинен закінчуватися на @gmail.com"
            )
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')
