from decouple import config
from django.contrib.auth.models import Group


class UserGroups:

    is_user = False
    user_group_name = ''
    is_admin = False
    admin_group_name = ''
    username = ''
    req = None

    def __init__(self, request):
        self.req = request
        if self.req.user.is_authenticated:
            self.username = self.req.user.username
        else:
            self.username = ''

        self.user_group_name = config('USERGROUP', default='xuser')
        self.admin_group_name = config('ADMINGROUP', default='xadmin')

        self.determine_groups()
        return

    def determine_groups(self):
        if self.username > '':
            # if you are an admin, then you are also a user
            self.is_admin = self.is_user_in_group(self.admin_group_name)
            if self.is_admin:
                self.is_user = True
            else:
                self.is_user = self.is_user_in_group(self.user_group_name)
        return

    def is_user_in_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            return self.req.user.groups.filter(id=group.id).exists()
        except Group.DoesNotExist:
            return False

    @property
    def not_user(self):
        return not self.is_user

    @property
    def not_admin(self):
        return not self.is_admin
