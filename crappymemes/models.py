from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Meme(models.Model):
    pic = models.ImageField(upload_to='images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)


class Comment(models.Model):
    meme = models.ForeignKey(Meme, null=False)
    message = models.CharField(max_length=256, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reply_to = models.ForeignKey('self', null=True)


class MemeLike(models.Model):
    value = models.SmallIntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    meme = models.ForeignKey(Meme, null=False)

    class Meta:
        unique_together = ('user', 'meme')


class CommentLike(models.Model):
    value = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=False)

    class Meta:
        unique_together = ('user', 'comment')


