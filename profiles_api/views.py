from rest_framework                 import status
from rest_framework.views           import APIView
from rest_framework                 import viewsets
from rest_framework.filters         import SearchFilter
from rest_framework.response        import Response
from rest_framework.authentication  import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions     import IsAuthenticated #IsAuthenticatedOrReadOnly
from rest_framework.settings        import api_settings

from .serializers import HelloSerializer, UserProfileSerializer, ProfileFeedItemSerializer
from .models      import UserProfile, ProfileFeedItem
from .permissions import UpdateOwnProfilePermission, UpdateOwnStatus


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = HelloSerializer          # What data to expect when making POST, PUT, PATCH, DELETE requests

    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name    = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message}, status=status.HTTP_201_CREATED)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viweset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viweset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name    = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message}, status=status.HTTP_201_CREATED)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Removing an object"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""

    serializer_class       = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes     = (UpdateOwnProfilePermission,)
    queryset               = UserProfile.objects.all()
    filter_backends        = (SearchFilter,)
    search_fields          = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user-authentication-tokens"""

    # Add renderer classes to the ObtainAuthToken view which will enable it at the DRF interface,
    #   the rest of the viewsets have it by default but the ObtainAuthToken doesn't
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""

    serializer_class       = ProfileFeedItemSerializer
    authentication_classes = (TokenAuthentication,)
    queryset               = ProfileFeedItem.objects.all()
    permission_classes     = (IsAuthenticated, UpdateOwnStatus)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
