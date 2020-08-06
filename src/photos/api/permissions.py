from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
	message = 'You must be the owner to make changes to the current object'

	def has_object_permission(self,request,view,obj):
		return obj.user == request.user
