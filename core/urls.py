"""dpunk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from core.views import home

from apps.posts.views import *
from apps.users.views import *
from apps.tests.views import *
from apps.users.managers import ACTIVATION_CODE_REGEX as ACR

from apps.posts.models import Post

urlpatterns = [

    url(r'^$', home, name='home'), # TODO: post_list, user_post_list

    url(r'^test/$',                          test,       name='test'),
    url(r'^start_test/(?P<test_id>\d+)/$',   start_test, name='start_test'),
    url(r'^end_test/$',                      end_test,   name='end_test'),

    url(r'^403/$', TemplateView.as_view(template_name='403.html'), name="403test"),
    url(r'^404/$', TemplateView.as_view(template_name='404.html'), name="404test"),
    url(r'^500/$', TemplateView.as_view(template_name='500.html'), name="500test"),

    url(r'^admin/', admin.site.urls),

    url(r'^login/$',                               user_login,            name='user_login'),
    url(r'^signup/$',                              user_signup,           name='user_signup'),
    url(r'^forgot_password/$',                     user_forgot_password,  name='user_forgot_password'),

    url(r'^user(?:/(?P<user_id>\d+))?/$$',         user_detail,           name='user_detail'),
    url(r'^edit/$',                                user_edit,             name='user_edit'),
    url(r'^send_activation/$',                     user_send_activation,  name='user_send_activation'),
    url(r'^change_email/$',                        user_change_email,     name='user_change_email'),
    url(r'^change_password/$',                     user_change_password,  name='user_change_password'),
    url(r'^delete/$',                              user_delete,           name='user_delete'),
    url(r'^logout/$',                              user_logout,           name='user_logout'),
    url(r'^new_password/(?P<code>'+ACR+r')/$',     user_new_password,     name='user_new_password'),
    url(r'^activation/(?P<code>'+ACR+r')/$',       user_activation,       name='user_activation'),

    # posts
    url(r'^post/add/$',                        post_form,    name='post_add',     kwargs={'model': Post, 'template': 'posts/post_form.html'}),
    url(r'^post/(?P<object_id>\d+)/$',         post_detail,  name='post_detail',  kwargs={'model': Post, 'template': 'posts/post_detail.html'}),
    url(r'^post/(?P<object_id>\d+)/edit/$',    post_form,    name='post_edit',    kwargs={'model': Post, 'template': 'posts/post_form.html'}),
    url(r'^post/(?P<object_id>\d+)/delete/$',  post_delete,  name='post_delete',  kwargs={'model': Post, 'template': 'posts/post_delete.html', 'redirect_name': 'user_detail'}),
    url(r'^post/(?P<object_id>\d+)/publish/$', post_publish, name='post_publish', kwargs={'model': Post}),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)