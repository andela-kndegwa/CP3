from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import permissions

from api.serializers import BucketListSerializer
from api.models import BucketList
from api.permissions import IsOwnerOrReadOnly
# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'buckelists': reverse('buckelists', request=request, format=format)
    })


class BucketListViewSet(viewsets.ModelViewSet):
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
