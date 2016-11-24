from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import permissions

from api.serializers import (BucketListSerializer,
                             BucketListItemSerializer, UserSerializer)
from api.models import BucketList, BucketListItem
from api.permissions import IsOwner, IsParentId

from django.contrib.auth.models import User

# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bucketlists': reverse('bucketlists', request=request, format=format),
        'items': reverse('items', request=request, format=format)
    })


class BucketListViewSet(viewsets.ModelViewSet):
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):
        queryset = request.user.bucketlists.all()
        serializer = BucketListSerializer(queryset,
                                          many=True,
                                          context={'request': Request(request)})
        return Response(serializer.data)


class BucketListItemViewSet(viewsets.ModelViewSet):
    queryset = BucketListItem.objects.all()
    serializer_class = BucketListItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsParentId)

    def perform_create(self, serializer):
        item_bucketlist_id = self.kwargs.get("bucketlist_pk")
        bucketlist = BucketList.objects.get(id=item_bucketlist_id)
        serializer.save(bucketlist=bucketlist)

    def get_queryset(self):
        """Limit items returned to those of a particular bucket list"""
        bucketlist_id = self.kwargs.get('bucketlist_pk')
        return BucketListItem.objects.filter(
            bucketlist=bucketlist_id,
            bucketlist__owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
