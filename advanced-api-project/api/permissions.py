from rest_framework.permissions import BasePermission

# Custom permission class to grant access to users who are Admins or Editors.
class IsAdminOrEditor(BasePermission):
    def has_permission(self, request, view):
        # Check if user is authenticated and has the role of 'admin' or 'editor'
        return request.user.is_authenticated and (request.user.role == 'editor' or request.user.role == 'admin')

# Custom permission class to grant access to users who are Admins.
class IsAdmin(BasePermission):

    # Permission Logic:
    def has_permission(self, request, view):
        
        # Check if user is authenticated and has the role of 'admin'
        return request.user.is_authenticated and request.user.role == 'admin'
