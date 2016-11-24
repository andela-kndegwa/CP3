from rest_framework import permissions

from api.models import BucketList


class IsParentId(permissions.BasePermission):
    """
    Permission does not permit access to bucket list item via
    bucket lists IDs that aren't owned by the current user
    """

    def has_permission(self, request, view):
        try:
            owner = BucketList.objects.get(
                pk=view.kwargs['bucketlist_pk']).owner
            return request.user == owner
        except BucketList.DoesNotExist:
            return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, BucketList):
            return obj.owner == request.user
