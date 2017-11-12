from django.db import models


# Create your models here.
class User(models.Model):
    display_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    super = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class TalkShow(models.Model):
    date = models.DateField()

    def __str__(self):
        return self.date


class Subject(models.Model):
    subject = models.CharField(max_length=255)
    date_added = models.DateTimeField()
    date_modified = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    talk_show_id = models.ForeignKey(TalkShow, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.subject


class TalkShowSubject(models.Model):
    talk_show_id = models.ForeignKey(TalkShow, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return TalkShowSubject.objects

# Create your models here.
