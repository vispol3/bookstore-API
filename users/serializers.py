from rest_framework import serializers

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')

        password = validated_data.pop('password', None)
        is_staff_requested = validated_data.pop('is_staff', False)
        user =  CustomUser(**validated_data)

        if request and request.user.is_staff:
            user.is_staff = is_staff_requested
        else:
            user.is_staff = False

        user.set_password(password)
        user.save()
        return user