from django.db import models
from .tools import Tools


# Create your models here.
class User(models.Model):
    display_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    super = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # Encrypt password in database
    def save(self, *args, **kwargs):
        self.password = Tools.md5(self.password)
        super(User, self).save()

    def __str__(self):
        return self.email


class TalkShow(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class Subject(models.Model):
    subject = models.CharField(max_length=255)
    date_added = models.DateTimeField()
    date_modified = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    talk_show_id = models.ForeignKey(TalkShow, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.subject


class TalkShowSubject(models.Model):
    talk_show_id = models.ForeignKey(TalkShow, on_delete=models.DO_NOTHING)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s: %s talked %s' % (str(self.talk_show_id.date), self.user_id.email, self.subject_id.subject)

# Create your models here.
