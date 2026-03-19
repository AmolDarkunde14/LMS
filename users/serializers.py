from rest_framework import serializers
from .models import User, MemberProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'first_name', 'last_name')

    def create(self, validated_data):
        request = self.context.get('request')
        # Public registration forces MEMBER role. Only Admin can create others.
        if not (request and request.user and request.user.is_authenticated and request.user.role == 'ADMIN'):
            validated_data['role'] = 'MEMBER'
            
        user = User.objects.create_user(**validated_data)
        if user.role == 'MEMBER':
            MemberProfile.objects.create(user=user)
        return user

class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MemberProfile
        fields = ('id', 'user', 'membership_date', 'max_books_allowed')
