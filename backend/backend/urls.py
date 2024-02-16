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

from django.urls import path
from . import settings
from . import views
from . import views_connection
from . import views_message
from . import views_user_relation
from . import views_achievement
from . import views_42link
from . import views_stats
from django.conf.urls.static import static


urlpatterns = [
    path("",views.index, name=""),
    path("profil/<str:pseudo>", views.otherProfilPage, name="otherProfilPage"),
    path("<int:num>", views.section, name="section"),
    path("getHeader", views.getHeader, name="getHeader"),

    path('gamePage/', views.gamePage, name='gamePage'),				#to remove at the end of project

    #User connection
    path("checkLogin", views_connection.checkLogin, name="checkLogin"),
    path("checkSignin", views_connection.checkSignin, name="checkSignin"),
    path("changePassword", views_connection.changePassword, name="changePassword"),
    path("changeUsername", views_connection.changeUsername, name="changeUsername"),

    #User relation
    path('addfriends', views_user_relation.addfriends, name='addfriends'),
    path('removefriends', views_user_relation.removefriends, name='removefriends'),
    path('block', views_user_relation.block, name='block'),
    path('unblock', views_user_relation.unblock, name='unblock'),
    path('acceptfriends', views_user_relation.acceptfriends, name='acceptfriends'),
    path('refusefriends', views_user_relation.refusefriends, name='refusefriends'),
    path('getrelation', views_user_relation.getrelation, name='getrelation'),
    path('getlistefriendrequest', views_user_relation.getlistefriendrequest, name='getlistefriendrequest'),
    path('getlistefriend', views_user_relation.getlistefriend, name='getlistefriend'),
    path('getlisteblocked', views_user_relation.getlisteblocked, name='getlisteblocked'),
    path('getcanbeinvited', views_user_relation.get_can_be_invited, name='get_can_be_invited'),

    #User achievement
    path('getselfachievement', views_achievement.getselfachievement, name='getselfachievement'),
    path('getotherachievement', views_achievement.getotherachievement, name='getotherachievement'),
    path('setachievement', views_achievement.setachievement, name='setachievement'),
    
    #User stats
    path('getuserstat', views_stats.getuserstat, name='getuserstat'),
    path('getwinrate', views_stats.getwinrate, name='getwinrate'),
    path('getusermatchhistory', views_stats.getusermatchhistory, name='getusermatchhistory'),
    
    #User message
    path("getMessages", views_message.getMessages, name="getMessages"),

    #User 42 connection
    path('checkislinked', views_42link.checkislinked, name='checkislinked'),
    path('removelink', views_42link.removelink, name='removelink'),

    # API
    path('api', views.apiDoc, name="api"),
    path('getUserViewById', views_connection.getUserViewById, name="getUserViewById")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
