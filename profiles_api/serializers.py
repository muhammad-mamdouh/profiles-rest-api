from rest_framework import serializers

from .models import UserProfile, ProfileFeedItem


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model  = UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = UserProfile.objects.create_user(
                email=validated_data['email'],
                name=validated_data['name'],
                password=validated_data['password']
        )
        
        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializers profile feed items"""

    class Meta:
        model        = ProfileFeedItem
        fields       = ('id', 'user_profile', 'status_text', 'created_on')  # id, created_on are automatically set by DB so by default they're read only
        extra_kwargs = {
            'user_profile': {'read_only': True}
        }
