# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class ModelDateTime(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        managed = False


class TblUser(User, ModelDateTime):
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    registered_from = models.IntegerField(default=1, help_text="1:Web, 2: Android, 3: IOS")
    is_paid = models.BooleanField(default=0)

    class Meta:
        db_table = 'tbl_user'


class TblNewsFeed(ModelDateTime):
    title = models.TextField(null=False, blank=False, default='')
    url = models.TextField(null=False, blank=False)
    hacker_news_url = models.TextField()
    posted_on = models.DateTimeField()
    upvotes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    total_blocked_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'tbl_news_feed'


class TblReadBlockNews(ModelDateTime):
    user = models.ForeignKey(User, null=False, blank=False)
    news_feed = models.ForeignKey(TblNewsFeed, on_delete=models.CASCADE, null=False, blank=False)
    action = models.IntegerField(default=1, help_text='1: read, 2:block')

    class Meta:
        unique_together = (('user', 'news_feed', 'action'),)
        db_table = 'tbl_read_block_news'
