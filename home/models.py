from django.db import models

# Create your models here.

class SystemInfo(models.Model):
    setting_name = models.CharField(max_length=50, null=True, blank=True)
    setting_text = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.setting_name + ' = ' + self.setting_text

    class Meta:
        ordering = ['setting_name']


class SessionData(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.CharField(max_length=50, null=True, blank=True)
    key_name = models.CharField(max_length=50, null=True, blank=True)
    key_text = models.CharField(max_length=2048, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session + ': ' + self.key_name + ' = ' + self.key_text

    class Meta:
        ordering = ['session', 'key_name']



class Sys_Settings:
    orgname = ""
    supportlink = ""
    allowed_domains = []
    default_email_from = ''

    # create constructor and initialize variables
    def __init__(self):
        self.orgname = self.get_orgname()
        self.supportlink = self.get_supportlink()
        self.allowed_domains = self.get_allowed_domains()
        self.default_email_from = self.get_default_email_from()

    # load orgname from SystemInfo
    def get_orgname(self):
        orgname = ''
        try:
            orgname = SystemInfo.objects.get(setting_name='orgname').setting_text
        except:
            pass
        return orgname

    # load supportlink from SystemInfo
    def get_supportlink(self):
        supportlink = ''
        try:
            supportlink = SystemInfo.objects.get(setting_name='supportlink').setting_text
        except:
            pass
        return supportlink

    # load allowed_domains from SystemInfo
    def get_allowed_domains(self):
        allowed_domains = ['secret_domain.com']
        try:
            allowed_domains = SystemInfo.objects.get(setting_name='allowed_domains').setting_text.split(',')
        except:
            pass
        return allowed_domains

    # load default_email_from from SystemInfo
    def get_default_email_from(self):
        default_email_from = 'user@domain.com'
        try:
            default_email_from = SystemInfo.objects.get(setting_name='default_email_from').setting_text
        except:
            pass
        return default_email_from


class SessionInfo(models.Model):
    record_id = models.IntegerField(default=0, blank=True, null=True)
    session_id = models.CharField(max_length=50, null=True, blank=True)
    key_name = models.CharField(max_length=50, null=True, blank=True)
    key_text = models.CharField(max_length=2048, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_id + ': ' + self.key_name + ' = ' + self.key_text

    class Meta:
        ordering = ['session_id', 'key_name']


class Session_Info_Data:
    session_id = ''
    session_data = {}

    def __init__(self, session_id):
        self.session_id = session_id
        self.session_info = SessionInfo.objects.filter(session_id=self.session_id)
        self.session_data = {}
        for session in self.session_info:
            self.session_data[session.key_name] = session.key_text

    def get_session_data(self, key):
        if key in self.session_data:
            return self.session_data[key]
        else:
            return ''

    def set_session_data(self, key, value):
        self.session_data[key] = value
        self.save_session_data()

    def remove_session_data(self, key):
        if key in self.session_data:
            del self.session_data[key]
            self.save_session_data()

    def save_session_data(self):
        for key in self.session_data:
            session = SessionInfo.objects.filter(session_id=self.session_id, key_name=key)
            if session:
                session = session[0]
                session.key_text = self.session_data[key]
                session.save()
            else:
                session = SessionInfo(session_id=self.session_id, key_name=key, key_text=self.session_data[key])
                session.save()


class UserSetting(models.Model):
    record_id = models.IntegerField(default=0, blank=True, null=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    key_name = models.CharField(max_length=50, null=True, blank=True)
    key_text = models.CharField(max_length=2048, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username + ': ' + self.key_name + ' = ' + self.key_text

    class Meta:
        ordering = ['username', 'key_name', 'key_text']

