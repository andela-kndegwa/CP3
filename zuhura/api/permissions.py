from rest_framework import permissions

from api.models import BucketList


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the bucket list.
        # or bucket list item resource
        return obj.owner == request.user


class IsOwnerOrReadOnlyItem(permissions.BasePermission):
    """
    Custom permission to only allow owners of a item to edit or
    delete it. Read only permission for non-owners of the item.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.bucketlist.owner == request.user


class IsParentId(permissions.BasePermission):
    """
    Permission does not permit access to bucketlist item via
    bucketlists IDs that aren't owned by the current user
    """

    def has_permission(self, request, view):
        try:
            owner = BucketList.objects.get(
                pk=view.kwargs['bucketlist_pk']).owner
            return request.user == owner
        except BucketList.DoesNotExist:
            return True
