# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_achievement.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/17 15:33:50 by lflandri          #+#    #+#              #
#    Updated: 2024/01/17 17:15:23 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hashlib, jwt, sys
import backend.settings as settings

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from db_test.models import User, Achivement
import datetime

from .forms import UserForm

from . import views
from .views import *

def createAchievementIfNot(user):
    """
    Return True if achievement existe or if it has been correctly created, return False else.
    """
    if len(Achivement.objects.all().filter(idUser=user.idUser)) > 0 :
        return True;
    try:
        achievement = Achivement(idUser=user)
        achievement.save()
        return True
    except :
        return False


def listAchievement(user):
    achievement = Achivement.objects.all().filter(idUser=user.idUser)[0]
    returnListe = [
    {
        "title" : "Winner",
        "description" : "win " + str(0) + "/" + str(((achievement.winner == 0) if 0 else ((achievement.winner == 1) if 1 else ((achievement.winner == 2) if 21 else 42)))) + " game.",
	    "grade" : achievement.winner
	},
    {
        "title" : "Perfect Shoot",
        "description" : "Do " + str(0) + "/" + str(((achievement.perfectShoot == 0) if 0 else ((achievement.perfectShoot == 1) if 1 else ((achievement.perfectShoot == 2) if 5 else 10)))) + " perfect shoot",
	    "grade" : achievement.perfectShoot
	},
    {
        "title" : "Bosco is your friend",
        "description" : "find bosco",
	    "grade" : achievement.boscoFriend
	},
    {
        "title" : "Dig your own grave",
        "description" : "marqué un but contre son camp",
	    "grade" : achievement.digGrave
	},
    {
        "title" : "To the fallen",
        "description" : "Pray for the fallen",
	    "grade" : achievement.fallen
	},
    {
        "title" : "Unpredictable",
        "description" : "Marqué " + str(0) + "/" + str(((achievement.unpredictable == 0) if 0 else ((achievement.unpredictable == 1) if 10 else ((achievement.unpredictable == 2) if 21 else 42)))) + " but avec rebond.",
	    "grade" : achievement.unpredictable
	},
    {
        "title" : "Faster than Shadow",
        "description" : "Parer une balle plus vite que " + str(0) + "/" + str(((achievement.faster == 0) if 0 else ((achievement.faster == 1) if 2 else ((achievement.faster == 2) if 3 else 4)))) + "",
	    "grade" : achievement.faster
	},
    {
        "title" : "A wave is in comming",
        "description" : "joué avec " + str(0) + "/" + str(((achievement.waveComming == 0) if 0 else ((achievement.waveComming == 1) if 2 else ((achievement.waveComming == 2) if 3 else 4)))) + " balle simultané ",
	    "grade" : achievement.waveComming
	},
    {
        "title" : "You shall not passed",
        "description" : "gagner " + str(0) + "/" + str(((achievement.notPassed == 0) if 0 else ((achievement.notPassed == 1) if 1 else ((achievement.notPassed == 2) if 21 else 42)))) + " match sans ce prendre de but",
	    "grade" : achievement.notPassed
	},
    {
        "title" : "You finaly find a friend !",
        "description" : "Have one friends",
	    "grade" : achievement.friend
	},
    {
        "title" : "Welcom to the party",
        "description" : "Jouer " + str(0) + "/" + str(((achievement.party == 0) if 0 else ((achievement.party == 1) if 1 else ((achievement.party == 2) if 21 else 42)))) + " match en equipe",
	    "grade" : achievement.party
	},
    {
        "title" : "Move your tin ass over here and hurry please!",
        "description" : "battre moly " + str(0) + "/" + str(((achievement.molyBatle == 0) if 0 else ((achievement.molyBatle == 1) if 1 else ((achievement.molyBatle == 2) if 21 else 42)))) + " fois.",
	    "grade" : achievement.molyBatle
	}
	]
    return returnListe


def setachievement(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    if not createAchievementIfNot(user) :
        return JsonResponse({"success": False, "content" : "Can't create achievement entry in db."})
    achievement = Achivement.objects.all().filter(idUser=user.idUser)[0]
    if request.POST.get('achievement') == "fallen":
        achievement.fallen = 4

    try :
        achievement.save()
    except :
        return JsonResponse({"success": False, "content" : "Can't change achievement entry in db."})

    return JsonResponse({"success": True, "content" : "Achievement entry changed."})

def getselfachievement(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    if not createAchievementIfNot(user) :
        return JsonResponse({"success": False, "content" : "Can't create achievement entry in db."})
    returnListe = listAchievement(user)
    return JsonResponse({"success": True, "content" : "", "listeAchievement" : returnListe})

def getotherachievement(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    # userId = check["userId"]
    # user = User.objects.all().filter(idUser=userId)[0]
    target = views.getTarget(request.POST.get('target'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    if not createAchievementIfNot(target) :
        return JsonResponse({"success": False, "content" : "Can't create achievement entry in db."})
    returnListe = listAchievement(target)
    return JsonResponse({"success": True, "content" : "", "listeAchievement" : returnListe})