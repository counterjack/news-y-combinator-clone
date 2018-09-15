"""


"""

import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from users.models import TblNewsFeed, TblReadBlockNews
from rest_framework import status
from django.db.models import Q

def login(request, *args, **kwargs):
	pass



def register(request, *args, **kwargs):
	pass



def home(*args, **kwargs):
	
	#news_feeds = TblReadBlockNews.objects.select_related('news_feed').values('news_feed__title', 'news_feed__url', 'news_feed__hacker_news_url', 'news_feed__posted_on', 'news_feed__upvotes', 'news_feed__total_comments').filter(~Q(action=2))
	blocked_feeds = TblReadBlockNews.objects.values_list('news_feed__id', flat=True).filter(action=2)
	news_feeds = TblNewsFeed.objects.all().exclude(id__in=blocked_feeds)
	
	print news_feeds

