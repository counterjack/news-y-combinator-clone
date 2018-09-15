# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class ModelDateTime(models.Model):
	created_on  = models.DateTimeField(auto_now=True)
	updated_on = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		abstract = True
		manage = False
	

class TblUser(User, ModelDateTime):
	phone = models.CharField(max_length=15, null=True, blank=True)
	gender = models.CharField(max_length=15, null=True, blank=True)
	dob = models.DateTimeField(null=True, blank=True)
	registered_from = models.IntegerField(default=1, help_text="1:Web, 2: Android, 3: IOS")
	is_paid = models.BooleanField(default=0)

	class Meta:
		db_table = 'tbl_user'



class TblNewsFeed(ModelDateTime):
	url = models.TextField()
	hacker_news_url = models.TextField()
	posted_on = models.DateTimeField()
	upvotes = models.IntegerField(default=0)
	total_comments = models.IntegerField(default=0)
	total_views = models.IntegerField(default=0)
	total_blocked_by = models.IntegerField(default=0)
	

	class Meta:
		db_table = 'tbl_news_feed'


class TblReadBlockNews(ModelDateTime):
	user = models.ForeignKey(TblUser, null=False, blank=False)
	news_feed = models.ForeignKey(TblNewsFeed, null=False, blank=False)
		
