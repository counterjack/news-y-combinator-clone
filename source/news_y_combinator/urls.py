"""news_y_combinator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users.views_cluster import login 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^news-feed/login/$', login._login),
    url(r'^news-feed/logout/$', login._logout),
    url(r'^news-feed/register/$', login.register),
    url(r'^news-feed/home/$', login.home),
    url(r'^news-feed/update-read-views/$', login.update_read_views),
    url(r'^news-feed/block-news-feed/$', login.read_block_news_feed),

]
