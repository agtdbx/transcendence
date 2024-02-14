# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_stats.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/02/14 16:40:22 by lflandri          #+#    #+#              #
#    Updated: 2024/02/14 17:47:49 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hashlib, jwt, sys
import backend.settings as settings

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from db_test.models import User, Match, Goal, MatchUser
import datetime

from .forms import UserForm
from .views_user_relation import getTarget

from . import views
from .views import *

def getWinRate(user):
    matchList = Match.objects.all().filter(idUser=user.idUser)
    win = 0
    for match in matchList :
        if MatchUser.objects.all().filter(idUser=user.idUser,idMatch=matchList)[0].idTeam == 1:
            if match.scoreLeft > match.scoreLeft :
                win+=1
        else :
            if match.scoreLeft < match.scoreLeft :
                win+=1
    return win / len(matchList)
                
        


def listStat(user):
    matchUserList = MatchUser.objects.all().filter(idUser=user.idUser)
    matchList = Match.objects.all().filter(idUser=user.idUser)
    matchListWithPowerUp = Match.objects.all().filter(idUser=user.idUser, powerUp=True)
    nbGoal = 0
    nbGoalCC = 0
    nbGoalWithoutBounce = 0
    nbMaxBallOnGame = 0
    for m in matchList:
        nbGoal += m.nbGoal
        nbGoalCC += m.nbCC
        if m.nbMaxBallOnGame > nbMaxBallOnGame :
            nbMaxBallOnGame = m.nbMaxBallOnGame    
    goalList = Goal.objects.all().filter(idUser=user.idUser)
    for g in goalList :
        if g.nbBounce == 0:
            nbGoalWithoutBounce+=1
    maxBallSpeed = 0
    maxBallBounce = 0
    for u in matchUserList :
        if u.maxBallSpeed > maxBallSpeed :
            maxBallSpeed =u.maxBallSpeed
        if u.maxBallBounce > maxBallBounce :
            maxBallBounce = u.maxBallBounce  
    return {
		"nbMatchPlayed":
        {
		  "nb":len(matchUserList),
		  "img": ""
	    },
		"nbMatchPlayedWithPowerUp":
        {
		  "nb":len(matchListWithPowerUp),
		  "img": ""
	    },
        "nbTournamentWin":
        {
		  "nb":user.nbTournamentWin,
		  "img": ""
	    }
        "nbGoal":
        {
		  "nb":nbGoal,
		  "img": ""
	    }
        "nbGoalCC":
        {
		  "nb":nbGoalCC,
		  "img": ""
	    }
        "nbGoalWithoutBounce":
        {
		  "nb":nbGoalWithoutBounce,
		  "img": ""
	    }
        "maxBallSpeed":
        {
		  "nb":maxBallSpeed,
		  "img": ""
	    }
        "maxBallBounce":
        {
		  "nb":maxBallBounce,
		  "img": ""
	    }
        "nbMaxBallOnGame":
        {
		  "nb":nbMaxBallOnGame,
		  "img": ""
	    }
	}
    
    