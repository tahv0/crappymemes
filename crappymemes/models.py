import json
from django.core import serializers
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
# Create your models here.


class CreatedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def created_mins_ago(self):
        now = datetime.now()
        then = self.created.replace(tzinfo=None)
        tdelta = now - then
        minutes = tdelta.seconds / 60
        return abs(int(minutes))

    class Meta:
        abstract = True


class Meme(CreatedModel):
    pic = models.ImageField(upload_to='images', null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)

    def comments_sum(self):
        return Comment.objects.filter(meme=self).count()

    def likes_sum(self):
        return MemeLike.objects.filter(meme=self).count()

    def get_likers(self):
        return User.objects.filter(memelike__meme=self)


    def get_likes_sum_by_month(self):
        qs = MemeLike.objects.filter(meme=self).annotate(date=TruncDate('created')
                                                           ).values('date').annotate(
            l=Count('pk')
        ).values('date', 'l').order_by('created')
        labels = []
        values = []
        for val in qs:
            labels.append(str(val['date']))
            values.append(val['l'])
        return {'labels': labels, 'values': values}

    def get_comments_sum_by_month(self):
        qs =  Comment.objects.filter(meme=self).annotate(date=TruncDate('created')
                                                           ).values('date').annotate(
            c=Count('pk')
        ).values('date', 'c').order_by('created')
        labels = []
        values = []
        for val in qs:
            labels.append(str(val['date']))
            values.append(val['c'])
        return {'labels': labels, 'values': values}


class Comment(CreatedModel):
    meme = models.ForeignKey(Meme, null=False)
    message = models.CharField(max_length=256, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    reply_to = models.ForeignKey('self', null=True)
    deleted = models.BooleanField(null=False, blank=False, default=False)

    def likes_sum(self):
        return CommentLike.objects.filter(comment=self).count()

    def get_likers(self):
        return User.objects.filter(commentlike__comment=self)

class MemeLike(CreatedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    meme = models.ForeignKey(Meme, null=False)
    class Meta:
        unique_together = ('user', 'meme')


class CommentLike(CreatedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=False)
    class Meta:
        unique_together = ('user', 'comment')


