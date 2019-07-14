from rest_framework import permissions

## default classes pasted from documentation ##

class BlacklistPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']

        # exists() is a boolean function
        blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()  #Blacklist is model that we never created!
        return not blacklisted


class IsOwnerOrReadOnly(permissions.BasePermission):

    message = "You must be the owner of this element to change it."

    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user



## ownly created classes ##

class AnonPermissionOnly(permissions.BasePermission):

    message = "already authenticated. Please log out to try again."

    """
    Non-authtenticated users only
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated



