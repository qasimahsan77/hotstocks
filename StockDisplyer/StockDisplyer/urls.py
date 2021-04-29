"""
Definition of urls for StockDisplyer.
"""

from datetime import datetime
from django.conf.urls import url
from django.conf.urls import include
import django.contrib.auth.views
from django.contrib import admin
from django.contrib import admindocs
import app.forms
import app.views
from app.views import login_user,home,signup,about,news
# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^news$', app.views.news, name='news'),
    url(r'^about', app.views.about, name='about'),
    url(r'^signup$', app.views.signup, name='signup'),
    #url(r'^login/$', django.contrib.auth.views.login, name='login'),
    url(r'^user_login/$',app.views.login_user,name="login"),
    #url(r'^user_login$',django.contrib.auth.views.LoginView.as_view(template_name="app/login_user.html"),name="login"),
    #url(r'^login$',django.contrib.auth.views.LoginView.as_view(template_name="app/login.html"),name="login"),
    url(r'^logout$',
        django.contrib.auth.views.LogoutView.as_view(template_name="app/login_user.html"),name='logout'),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', 'django.contrib.admindocs.urls'),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', admin.site.urls)
]