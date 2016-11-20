from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import permissions

from api.serializers import BucketListSerializer, BucketListItemSerializer
from api.models import BucketList, BucketListItem
from api.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyItem
# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'buckelists': reverse('buckelists', request=request, format=format),
        'items': reverse('items', request=request, format=format)
    })


class BucketListViewSet(viewsets.ModelViewSet):
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BucketListItemViewSet(viewsets.ModelViewSet):
    queryset = BucketListItem.objects.all()
    serializer_class = BucketListItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnlyItem)

    def perform_create(self, serializer):
        print(serializer)
        item_bucketlist_id = self.kwargs.get("bucketlist_pk")
        bucketlist = BucketList.objects.get(id=item_bucketlist_id)
        serializer.save(bucketlist=bucketlist)

    def get_queryset(self):
        """Limit items returned to those of a particular bucketlist"""
        bucketlist_id = self.kwargs.get('bucketlist')
        return BucketListItem.objects.filter(
            bucketlist=bucketlist_id,
            bucketlist__owner=self.request.user)
