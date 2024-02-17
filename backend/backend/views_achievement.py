# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_achievement.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <liam.flandrinck.58@gmail.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/17 15:33:50 by lflandri          #+#    #+#              #
#    Updated: 2024/02/17 18:50:38 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hashlib, jwt, sys
import backend.settings as settings

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from db_test.models import User, Achivement, Match, MatchUser
import datetime

from .forms import UserForm

from . import views
from .views import *

def getTarget(targetName):
    """
    return the user object in db who have targetName as username, if there is not user with this username, return None
    """
    targetListe = User.objects.all().filter(username=targetName)
    if len(targetListe) > 0:
        return targetListe[0]
    return None

def getListeMatchDataForAchievement(user):
    #declare variable
    maxBallSpeed = 0
    maxBallBounce = 0
    nbPerfectShoot = 0
    nbGoalCC = 0
    nbMaxBallOnGame = 0
    nbwinWithoutTakeGoal = 0
    win = 0
    nbMatchInTeam = 0
    nbBoscoBeDestroy = 0

    matchUserList = MatchUser.objects.all().filter(idUser=user.idUser)
    matchList = []
    for usermatch in matchUserList :
        matchList += Match.objects.all().filter(matchuser=usermatch)

    for m in matchList: #get info from match
        if m.type > 2 :
            continue
        if m.nbMaxBallOnGame > nbMaxBallOnGame :
            nbMaxBallOnGame = m.nbMaxBallOnGame
        if MatchUser.objects.all().filter(idUser=user.idUser,idMatch=m.idMatch)[0].idTeam == 1:
            if m.scoreRight > m.scoreLeft :
                win+=1
                if m.scoreLeft == 0 :
                    nbwinWithoutTakeGoal+=1
                if len(MatchUser.objects.all().filter(idTeam=1,idMatch=m.idMatch)) > 1:
                   nbMatchInTeam+=1
                if len(MatchUser.objects.all().filter(idTeam=0,idMatch=m.idMatch, idUser__lt=0)) > 0 :
                    nbBoscoBeDestroy+=1
        else :
            if m.scoreRight < m.scoreLeft :
                win+=1
                if m.scoreRight == 0 :
                    nbwinWithoutTakeGoal+=1
                if len(MatchUser.objects.all().filter(idTeam=0,idMatch=m.idMatch)) > 1:
                   nbMatchInTeam+=1
                if len(MatchUser.objects.all().filter(idTeam=1,idMatch=m.idMatch, idUser__lt=0)) > 0 :
                    nbBoscoBeDestroy+=1

    for u in matchUserList : #get info from matchuser
        if u.idMatch.type > 2 :
            continue
        nbPerfectShoot += u.nbPerfectShot
        nbGoalCC += u.nbCC
        if u.maxBallSpeed > maxBallSpeed :
            maxBallSpeed =u.maxBallSpeed
        if u.maxBallBounce > maxBallBounce :
            maxBallBounce = u.maxBallBounce

    return [win, nbPerfectShoot, nbGoalCC, maxBallBounce,
            maxBallSpeed, nbMaxBallOnGame, nbwinWithoutTakeGoal,
            nbMatchInTeam, nbBoscoBeDestroy]

def createAchievementIfNot(user):
    """
    Return True if achievement existe or if it has been correctly created,
    return False else.
    """
    if len(Achivement.objects.all().filter(idUser=user.idUser)) > 0 :
        return True;
    try:
        achievement = Achivement(idUser=user)
        achievement.save()
        return True
    except :
        return False


def listAchievement(user, isself):
    achievement = Achivement.objects.all().filter(idUser=user.idUser)[0]
    imgPath = "/static/image/achievement/"
    if isself :
        errorDescription = "You don't have this achievement"
    else :
        errorDescription = "This player doesn't have this achievement"
    errorName = "ERR://23¤Y%/ "
    listData = getListeMatchDataForAchievement(user)
    returnListe = [
    {
        "title" : "Winner" if (achievement.winner > 0) else errorName,
        "description" :  (errorDescription if (achievement.winner == 0) else "win " + str(listData[0]) + "/" + ( '1' if (achievement.winner == 1) else ( '21' if (achievement.winner == 2) else '42')) + " game."),
        "grade" : achievement.winner,
        "img" : imgPath + ("Winner.webp" if (achievement.winner > 0) else "Error.webp")
    },
    {
        "title" :  "Perfect Shoot" if achievement.perfectShoot > 0   else errorName,
        "description" :  (errorDescription  if (achievement.perfectShoot == 0) else "Do " + str(listData[1]) + "/" + ( '1' if (achievement.perfectShoot == 1) else ( '5' if (achievement.perfectShoot == 2) else '10')) + " perfect shoot"),
        "grade" : achievement.perfectShoot,
        "img" : imgPath + ( "PerfectShoot.webp" if achievement.perfectShoot > 0  else "Error.webp")
    },
    {
        "title" : "Bosco is your friend" if achievement.boscoFriend > 0 else errorName,
        "description" : "Find bosco." if achievement.boscoFriend > 0 else errorDescription,
        "grade" : achievement.boscoFriend,
        "img" : imgPath + ("bosco_move.gif" if achievement.boscoFriend > 0  else "Error.webp")
    },
    {
        "title" : "Dig your own grave" if achievement.digGrave > 0 else errorName,
        "description" :"Scored an own goal." if achievement.digGrave  > 0 else errorDescription,
        "grade" : achievement.digGrave,
        "img" : imgPath + ("GraveDig.webp" if achievement.digGrave > 0  else "Error.webp")
    },
    {
        "title" : "To the fallen" if achievement.fallen > 0 else errorName,
        "description" :  "Pray for the fallen." if achievement.fallen > 0 else errorDescription,
        "grade" : achievement.fallen,
        "img" : imgPath + ( "Fallen.webp" if achievement.fallen > 0 else "Error.webp")
    },
    {
        "title" : "Unpredictable" if achievement.unpredictable > 0 else errorName,
        "description" : (errorDescription if (achievement.unpredictable == 0) else "Scored goal with " + str(listData[3]) + "/" +  ( '10' if (achievement.unpredictable == 1) else ( '21' if (achievement.unpredictable == 2) else '42')) + " bound."),
        "grade" : achievement.unpredictable,
        "img" : imgPath + ("Unpredictable.webp" if achievement.unpredictable > 0  else "Error.webp")
    },
    {
        "title" : "Faster than Shadow" if achievement.faster > 0 else errorName,
        "description" :  (errorDescription if (achievement.faster == 0) else "Parer une balle plus vite que " + str(listData[4]) + "/" + ('1000' if (achievement.faster == 1) else ('1920' if (achievement.faster == 2) else '4242')) + "."),
        "grade" : achievement.faster,
        "img" : imgPath + ("Faster.webp" if achievement.faster > 0 else "Error.webp")
    },
    {
        "title" : "A wave is in comming" if achievement.waveComming > 0 else errorName,
        "description" :  (errorDescription if (achievement.waveComming == 0) else "Play with " + str(listData[5]) + "/" + ('2' if (achievement.waveComming == 1) else ('4' if (achievement.waveComming == 2) else '8')) + " ball at the ame time."),
        "grade" : achievement.waveComming,
        "img" : imgPath + ("WaveCommig.webp" if  achievement.waveComming > 0 else "Error.webp")
    },
    {
        "title" : "You shall not passed" if achievement.notPassed > 0 else errorName,
        "description" :  (errorDescription if (achievement.notPassed == 0) else "Win " + str(listData[6]) + "/" + ('1' if (achievement.notPassed == 1) else ('21' if (achievement.notPassed == 2) else '42')) + " without taking a goal."),
        "grade" : achievement.notPassed,
        "img" : imgPath + ("NotPassed.webp" if achievement.notPassed > 0  else "Error.webp")
    },
    {
        "title" : "You finaly find a friend !" if achievement.friend > 0 else errorName,
        "description" : "Have one friends." if achievement.friend > 0 else errorDescription,
        "grade" : achievement.friend,
        "img" : imgPath + ("Friend.webp" if achievement.friend > 0  else "Error.webp")
    },
    {
        "title" : "Welcom to the party" if achievement.party > 0 else errorName,
        "description" :  (errorDescription if (achievement.party == 0) else "Play " + str(listData[7]) + "/" + ('1' if (achievement.party == 1) else ('21' if (achievement.party == 2) else '42')) + " match in team."),
        "grade" : achievement.party,
        "img" : imgPath + ("Party.webp" if achievement.party > 0 else "Error.webp")
    },
    {
        "title" : "APD-B317 desactivated" if achievement.molyBattle > 0 else errorName,
        "description" :  (errorDescription if (achievement.molyBattle == 0) else "Win over Bosco " + str(listData[8]) + "/" + ('1' if (achievement.molyBattle == 1) else ('21' if (achievement.molyBattle == 2) else '42'))) + " times.",
        "grade" : achievement.molyBattle,
        "img" : imgPath + ("APD-B317.png" if achievement.molyBattle > 0  else "Error.webp")
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
    if request.POST.get('achievement') == "boscoFriend":
        achievement.boscoFriend = 4

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
    returnListe = listAchievement(user, True)
    return JsonResponse({"success": True, "content" : "", "listeAchievement" : returnListe})

def getotherachievement(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    # userId = check["userId"]
    # user = User.objects.all().filter(idUser=userId)[0]
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    if not createAchievementIfNot(target) :
        return JsonResponse({"success": False, "content" : "Can't create achievement entry in db."})
    returnListe = listAchievement(target, False)
    return JsonResponse({"success": True, "content" : "", "listeAchievement" : returnListe})
