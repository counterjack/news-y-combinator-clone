# -*- encoding: utf-8 -*-
"""

"""

import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from users.models import TblNewsFeed, TblReadBlockNews, TblUser


@csrf_exempt
# @api_view(['GET', 'POST'])
def _login(request, *args, **kwargs):
	if request.user.is_authenticated:
		return redirect('/news-feed/home/')

	if request.method == 'GET':
		return render(request, 'users/login.html', context={})

	content = {
		'status': 0,
		'message': 'Invalid Request',
		'response_code': status.HTTP_400_BAD_REQUEST,
		'data': []
	}

	json_data = json.loads(request.body)
	username = json_data.get('username', None)
	password = json_data.get('password', None)
	if not (username and password):
		return JsonResponse(content)
	# validate user to be genuine
	user = authenticate(username=username, password=password)
	if not user:
		content.update({
			'message': 'Invalid Username or Password'
		})
		return JsonResponse(content)
	# creating user session
	if user is not None:
		login(request, user)
		content.update({
			'status': 1,
			'response_code': status.HTTP_200_OK,
			'message': 'authenticated successfully'
		})
		return JsonResponse(content, safe=False)


@api_view(['GET'])
def _logout(request, *args, **kwargs):
	logout(request)
	return redirect('/news-feed/login/')


@api_view(['POST'])
def register(request, *args, **kwargs):
	content = {
		'status': 0,
		'message': 'Invalid Request',
		'error': '',
		'response_code': status.HTTP_400_BAD_REQUEST,
		'data': []
	}
	json_data = request.body

	username = json_data.get('username', None)
	password = json_data.get('password', None)
	email = json_data.get('email', None)
	phone = json_data.get('phone', None)
	if not (username and password and email and phone):
		return Response(content)

	try:
		tbl_user = TblUser.objects.create(username=username, password=password, email=email, is_active=True)

	except Exception as e:
		error = e
		content.update({'error': error})
	return Response(content)


@login_required()
@api_view(['GET'])
def home(request, *args, **kwargs):
	blocked_feeds = TblReadBlockNews.objects.values_list('news_feed__id', flat=True).filter(action=2, user=request.user)
	news_feeds = TblNewsFeed.objects.all().values('id', 'title', 'url', 'hacker_news_url', 'posted_on', 'upvotes',
												  'total_comments').exclude(id__in=blocked_feeds)
	return render(request, 'users/home.html', {
		'news_feeds': news_feeds
	})


# @api_view(['POST'])
@csrf_exempt
def update_read_views(request, *args, **kwargs):
	content = {
		'status': 0,
		'message': 'Invalid Request',
		'error': '',
		'response_code': status.HTTP_400_BAD_REQUEST,
		'data': []
	}

	json_data = json.loads(request.body)
	news_feed_id = json_data['news_id']
	try:
		feed = TblNewsFeed.objects.get(id=news_feed_id)
		feed.total_views += 1
		feed.save()
		content.update({
			'status': 1,
			'message': 'Views updated',
			'response_code': status.HTTP_200_OK
		})
		return JsonResponse(content)

	except ObjectDoesNotExist:
		print 'error'
		content.update({
			'message': 'Invalid POST ID'
		})
		return JsonResponse(content)


@csrf_exempt
def read_block_news_feed(request, *args, **kwargs):
	content = {
		'status': 0,
		'message': 'Invalid Request',
		'error': '',
		'response_code': status.HTTP_400_BAD_REQUEST,
		'data': []
	}

	json_data = json.loads(request.body)
	news_feed_id = json_data['news_id']
	action = json_data.get('action', None)  # 1: mark read, 2 : block
	try:
		feed = TblNewsFeed.objects.get(id=news_feed_id)
	except ObjectDoesNotExist:
		content.update({
			'message': 'Invalid POST ID'
		})
		return JsonResponse(content)
	try:
		read_block_news = TblReadBlockNews.objects.get(user=request.user, action=action, news_feed=feed)
		content.update({
			'message': 'Already Blocked for the user'
		})
		return JsonResponse(content)
	except:
		TblReadBlockNews.objects.create(user=request.user, news_feed=feed, action=action)
		if action == 2:
			feed.total_blocked_by += 1
			feed.save()
		content.update({
			'status': 1,
			'message': 'Successfully',
			'response_code': status.HTTP_200_OK
		})
		return JsonResponse(content)
