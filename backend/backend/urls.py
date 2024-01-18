"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    path("",views.index, name=""),
    path("profil/<str:pseudo>", views.otherProfilPage, name="otherProfilPage"),
    path("<int:num>", views.section, name="section"),
    path("getHeader", views.getHeader, name="getHeader"),
    path("checkLogin", views.checkLogin, name="checkLogin"),
    path("checkSignin", views.checkSignin, name="checkSignin"),
    path('gamePage/', views.gamePage, name='gamePage'),                #to remove at the end of project

    path('addfriends', views.addfriends, name='addfriends'),
    path('removefriends', views.removefriends, name='removefriends'),
    path('block', views.block, name='block'),
    path('unblock', views.unblock, name='unblock'),
    path('acceptfriends', views.acceptfriends, name='acceptfriends'),
    path('refusefriends', views.refusefriends, name='refusefriends'),
    path('getrelation', views.getrelation, name='getrelation'),
    path('getlistefriendrequest', views.getlistefriendrequest, name='getlistefriendrequest'),
    path('getlistefriend', views.getlistefriend, name='getlistefriend'),
    path('getlisteblocked', views.getlisteblocked, name='getlisteblocked'),

    path("getMessages", views.getMessages, name="getMessages"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
