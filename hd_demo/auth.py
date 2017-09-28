from hd_mesos.models import Users
from rest_framework import authentication
from rest_framework import exceptions

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.get('username')
        print request.data,username
        if not username:
            return None

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
