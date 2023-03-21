from .models import UserSetting

class UserSettings:
    username = ''
    settings = {}

    def __init__(self, username=''):
        self.username = username
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        settings = UserSetting.objects.filter(username=self.username)
        for setting in settings:
            self.settings[setting.key_name] = setting.key_text
