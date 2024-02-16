# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_stats.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <liam.flandrinck.58@gmail.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/02/14 16:40:22 by lflandri          #+#    #+#              #
#    Updated: 2024/02/16 04:01:52 by lflandri         ###   ########.fr        #
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

def createListGoal(player, match):
    goalListe = Goal.objects.all().filter(idMatch=match, idUser=player.idUser).order_by("goalTime")
    listGoal = []
    for goal in goalListe :
        listGoal.append({
            "time" : goal.goalTime / 60,
            "bounce" : goal.nbBounce,
            "speed": goal.ballSpeed
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
        playerList = MatchUser.objects.all().filter(idMatch=match.idMatch)
        for player in playerList :
            if player.idTeam == 1 :
                playerNomination = "playerR" + str(countUserRight)
                countUserRight+=1
            else :
                playerNomination = "playerL" + str(countUserLeft)
                countUserLeft+=1 
            toAdd[playerNomination] = {
                "name": player.idUser.username,
                "pp": "/static/" + player.idUser.profilPicture.name,
                "goalList":createListGoal(player, match)
            }
        matchListReturn.append(toAdd)
    return JsonResponse({"success": True, "content" : matchListReturn})
            
    
    
    
		# "player1" :
		# {
		# 	"name" : "Enginer",
		# 	"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/4/46/Engineer_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150041",
		# 	"goalList":
		# 	[
		# 		{"time" : 0.50, "bounce" : 0, "speed": 0.15},
		# 		{"time" : 1.5, "bounce" : 1, "speed": 0.15},
		# 		{"time" : 2.35689, "bounce" : 15, "speed": 0.15},
		# 		{"time" : 4.50, "bounce" : 6, "speed": 0.15},
		# 		{"time" : 4.70, "bounce" : 999, "speed": 10},  
		# 		{"time" : 6.56, "bounce" : 2, "speed": 0.15},
		# 		{"time" : 7, "bounce" : 3, "speed": 0.15},
		# 		{"time" : 9, "bounce" : 6, "speed": 1},
		# 		{"time" : 12, "bounce" : 8, "speed": 0.15},
		# 		{"time" : 13, "bounce" : 5, "speed": 0.15},
		# 		{"time" : 18.95, "bounce" : 3, "speed": 0.15}
		# 	]
		# },