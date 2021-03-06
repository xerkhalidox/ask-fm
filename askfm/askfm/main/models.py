from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class custom_user(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    gender = models.BooleanField()
    avatar = models.CharField(max_length=200)


class Question(models.Model):
    question = models.CharField(max_length=300)
    is_anon = models.BooleanField()
    is_answered = models.BooleanField()
    user_asks = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_asked = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='que_asked', on_delete=models.CASCADE)


class Answer(models.Model):
    answer = models.TextField()
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'follower'),)

class Question_Notification(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    is_read=models.BooleanField()

class Answer_Notification(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE)
    is_read=models.BooleanField()