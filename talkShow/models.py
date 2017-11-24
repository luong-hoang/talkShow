from django.db import models
from django.utils import timezone

from .tools import Tools


# Create your models here.
class User(models.Model):
    display_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    super = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # In any given moment, 1 user can has only 1 new subject
    def can_add_more_subject(self):
        subjects = self.subject_set.all()
        for subject in subjects:
            if not subject.talked():
                return False
        return True

    # Encrypt password in database
    def save(self, update_pass=True, *args, **kwargs):
        if update_pass:
            self.password = Tools.md5(self.password)
        super(User, self).save(*args, **kwargs)

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
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def talked(self):
        if self.talkshowsubject_set.count() > 0:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        # from django.core.exceptions import FieldError
        # raise FieldError('Test exception')
        self.date_modified = timezone.now()
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject


class TalkShowSubject(models.Model):
    talk_show = models.ForeignKey(TalkShow, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s: %s talked %s' % (str(self.talk_show.date), self.user.email, self.subject.subject)

# Create your models here.
