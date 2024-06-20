from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username','password','email', 'telephone'
        )
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data["username"],
            telephone=validated_data["telephone"]
        )
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user