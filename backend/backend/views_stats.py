# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_stats.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/02/14 16:40:22 by lflandri          #+#    #+#              #
#    Updated: 2024/02/17 02:27:56 by aderouba         ###   ########.fr        #
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
    matchUserList = MatchUser.objects.all().filter(idUser=user.idUser)
    matchList = []
    for usermatch in matchUserList :
        matchList += Match.objects.all().filter(matchuser=usermatch)
    if len(matchList) == 0:
        return None
    win = 0
    for match in matchList :
        if MatchUser.objects.all().filter(idUser=user.idUser,idMatch=match.idMatch)[0].idTeam == 1:
            if match.scoreRight > match.scoreLeft :
                win+=1
        else :
            if match.scoreRight < match.scoreLeft :
                win+=1
    return win / len(matchList)




def listStat(user):
    matchUserList = MatchUser.objects.all().filter(idUser=user.idUser)
    matchList = []
    matchListWithPowerUp = []
    for usermatch in matchUserList :
        matchList += Match.objects.all().filter(matchuser=usermatch)
        matchListWithPowerUp += Match.objects.all().filter(matchuser=usermatch, powerUp=True)
    nbGoalWithoutBounce = 0
    nbMaxBallOnGame = 0
    for m in matchList:
        if m.nbMaxBallOnGame > nbMaxBallOnGame :
            nbMaxBallOnGame = m.nbMaxBallOnGame
    goalList = Goal.objects.all().filter(idUser=user.idUser)
    for g in goalList :
        if g.nbBounce == 0:
            nbGoalWithoutBounce+=1
    maxBallSpeed = 0
    maxBallBounce = 0
    nbGoal = 0
    nbGoalCC = 0
    for u in matchUserList :
        nbGoal += u.nbGoal
        nbGoalCC += u.nbCC
        if u.maxBallSpeed > maxBallSpeed :
            maxBallSpeed =u.maxBallSpeed
        if u.maxBallBounce > maxBallBounce :
            maxBallBounce = u.maxBallBounce
    return [
        {
		  "description":"number of match played :" + str(len(matchUserList)),
		  "img": ""
	    },
        {
		  "description":"number of match played with power up :" + str(len(matchListWithPowerUp)),
		  "img": ""
	    },
        {
		  "description":"number of tournament win :" + str(user.nbTournamentWin),
		  "img": ""
	    },
        {
		  "description":"number of goals scored : " + str(nbGoal),
		  "img": ""
	    },
        {
		  "description":"number of goals scored against yourself : " + str(nbGoalCC),
		  "img": ""
	    },
        {
		  "description":"number of goals scored without bounce : " + str(nbGoalWithoutBounce),
		  "img": ""
	    },
        {
		  "description":"maximum ball speed parried : " + str(maxBallSpeed),
		  "img": ""
	    },
        {
		  "description":"record of bounce before a goal : " + str(maxBallBounce),
		  "img": ""
	    },
        {
		  "description":"maximun ball on the field : " + str(nbMaxBallOnGame),
		  "img": ""
	    }
	]

def getwinrate(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    return JsonResponse({"success": True, "content" : getWinRate(target)})

def getuserstat(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    return JsonResponse({"success": True, "content" : listStat(target)})

def createListGoal(player : MatchUser, match):
    goalListe = Goal.objects.all().filter(idMatch=match, idUser=player.idUser, idTeam=player.idTeam).order_by("goalTime")
    listGoal = []
    username = player.idUser.username
    if username == "bosco":
        if player.idTeam == 0:
            username += " left"
        else:
            username += " right"

    for goal in goalListe :
        listGoal.append({
            "username" : username,
            "time" : goal.goalTime / 60,
            "bounce" : goal.nbBounce,
            "speed": goal.ballSpeed,
            "ownGoal" : goal.ownGoal
            })
    return listGoal


def getusermatchhistory(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)
    user = getTarget(request.POST.get('friend'))
    if user == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    matchUserList = MatchUser.objects.all().filter(idUser=user.idUser)
    matchList = []
    for usermatch in matchUserList :
        matchList += Match.objects.all().filter(matchuser=usermatch)
    matchListReturn = []
    for match in matchList :
        countUserLeft = 1
        countUserRight = 1
        toAdd = {}
        toAdd["duration"] = match.matchDuration / 60
        toAdd["powerUp"] = match.powerUp
        toAdd["map"] = match.idMap.name
        toAdd["scoreLeft"] = match.scoreLeft
        toAdd["scoreRight"] = match.scoreRight
        playerList = MatchUser.objects.all().filter(idMatch=match.idMatch)
        for player in playerList :
            if player.idTeam == 1 :
                playerNomination = "playerR" + str(countUserRight)
                countUserRight+=1
                if player.idUser == user:
                    if match.scoreRight > match.scoreLeft:
                        toAdd["result"] = "win"
                    else:
                        toAdd["result"] = "lose"
            else :
                playerNomination = "playerL" + str(countUserLeft)
                countUserLeft+=1
                if player.idUser == user:
                    if match.scoreRight < match.scoreLeft:
                        toAdd["result"] = "win"
                    else:
                        toAdd["result"] = "lose"
            toAdd[playerNomination] = {
                "name": player.idUser.username,
                "pp": "/static/" + player.idUser.profilPicture.name,
                "goalList":createListGoal(player, match)
            }
        matchListReturn.append(toAdd)
    return JsonResponse({"success": True, "content" : matchListReturn})
