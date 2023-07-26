from .models import UserSetting

class UserSettings:
    username = ''
    settings = {}

    def __init__(self, username=''):
        self.username = username
        self.settings = {}
        self.__set_default_settings__()
        self.load_settings()

    def __set_default_settings__(self):
        self.settings = {
            "rows_per_page": 10,
            "show_only_active_parcels": True,
        }
        return

    def load_settings(self):
        settings = UserSetting.objects.filter(username=self.username)
        for setting in settings:
            self.settings[setting.key_name] = setting.key_text

