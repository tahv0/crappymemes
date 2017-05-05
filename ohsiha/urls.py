"""ohsiha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout
from django.conf.urls.static import static
from django.contrib import admin
from crappymemes import views as memeviews


urlpatterns = [
    url(r'^$', memeviews.home, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^meme/(?P<meme_id>\d+)/edit/$', memeviews.EditMeme.as_view(), name='edit_meme'),
    url(r'^meme/(?P<meme_id>\d+)/like/$', memeviews.LikeMeme.as_view(), name='like_meme'),
    url(r'^meme/(?P<meme_id>\d+)/delete/$', memeviews.DeleteMeme.as_view(), name='delete_meme'),
    url(r'^comment/(?P<comment_id>\d+)/like/$', memeviews.LikeComment.as_view(),
        name='like_comment'),
    url(r'meme/(?P<meme_id>\d+)/comment/(?P<comment_id>\d+)/delete/$', memeviews.DeleteComment.as_view(), name='delete_comment'),
    url(r'^meme/(?P<meme_id>\d+)/comment/(?P<comment_id>\d+)/$', memeviews.ReplyComment.as_view(), name='reply_comment'),
    url(r'^meme/(?P<meme_id>\d+)/comment/$', memeviews.AddComment.as_view(), name='add_comment'),
    url(r'^meme/(?P<meme_id>\d+)/likes/$', memeviews.MemeLikeChart.as_view(), name='meme_likes'),
    url(r'^meme/(?P<meme_id>\d+)/comments/$', memeviews.MemeCommentChart.as_view(), name='meme_comments'),
    url(r'^meme/(?P<meme_id>\d+)/$', memeviews.ShowMeme.as_view(), name='show_meme'),
    url(r'^meme/$', memeviews.NewMeme.as_view(), name='add_meme'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^settings/$', memeviews.settings, name='settings'),
    url(r'^settings/password/$', memeviews.password, name='password'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
