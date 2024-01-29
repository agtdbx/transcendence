# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2024/01/29 14:06:34 by hde-min          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import  os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from db_test.models import User
import datetime

from .forms import UserForm
from .views_connection import checkToken
from .views_connection import checkApi42Request


# **************************************************************************** #
#                                 Page Function                                #
# **************************************************************************** #
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def getHeader(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    test = User.objects.all().filter(idUser=userId)

    if len(test) != 1:
        return JsonResponse({"success" : False, "error" : "User not found"})

    user = test[0]

    htmlText = render(request,"navbar.html", {'user': user}).getvalue().decode()
    return JsonResponse({"success" : True, "html" : htmlText})


@csrf_exempt
def otherProfilPage(request, pseudo):
    check = checkToken(request)
    if check["success"] == False:
        return render(request, "index.html")
    try :
        fullPage = (request.method != 'POST')

        test = User.objects.all().filter(username=pseudo)
        if len(test) == 0:
            if fullPage:
                return render(request, "mainpage_full.html")
            else:
                return render(request,"mainpage.html")

        userToVisit = test[0]
        user = User.objects.all().filter(idUser=check["userId"])[0]

        if user == userToVisit:
            if fullPage:
                return render(request, "profil_content_full.html", {'user': user})
            else:
                return render(request,"profil_content.html", {'user': user})

        if fullPage:
            return render(request, "other_profil_content_full.html", {'user': userToVisit})
        else:
            return render(request,"other_profil_content.html", {'user': userToVisit})
    except :
        return render(request, "mainpage.html")


@csrf_exempt
def section(request, num):
    """
    Args:
        request (_type_): The request
        num (_type_): Which page to load

    Returns:
        The page to render
        The login page is the token is invalid
        The main page if the num page doesn't exist
    """
    fullPage = (request.method != 'POST')

    if num == 0:
        if fullPage:
            return render(request, "index.html")
        else:
            return render(request, "index_spa.html")

    elif num == 1:
        if fullPage:
            return render(request, "signin_full.html")
        else:
            return render(request, "signin.html")

    elif num == 2:
        if fullPage:
            return render(request, "login_full.html")
        else:
            return render(request, "login.html")

    #conecting with 42 api
    elif num == 3 and fullPage and request.GET.get('code', None) != None:
        return checkApi42Request(request, True, None)


    # Check token
    check = checkToken(request)
    if check["success"] == False:
        if fullPage:
            return render(request, "login_full.html")
        else:
            return render(request, "login.html")

    # Get the user
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]

    if num == 3:
        if fullPage:
            return render(request, "mainpage_full.html")
        else:
            return render(request, "mainpage.html")

    elif num == 4:
        if fullPage:
            return render(request, "mainpage_full.html")
        else:
            return render(request,"waitpage.html")

    elif num == 5:
        if fullPage:
            return render(request, "createGameRoom_full.html")
        else:
            return render(request,"createGameRoom.html")

    elif num == 6:
        if fullPage:
            return render(request, "mainpage_full.html")
        else:
            return render(request,"game.html")

    elif num == 7:
        if fullPage:
            return render(request, "tournament_full.html")
        else:
            return render(request,"tournament.html")

    elif num == 8:
        if fullPage:
            return render(request, "tournamentcreate_full.html")
        else:
            return render(request,"tournamentcreate.html")

    elif num == 9:
        if fullPage and request.GET.get('code', None) != None:
            return checkApi42Request(request, False, user)
        elif fullPage :
            return render(request, "profil_content_full.html", {'user': user})
        else:
            return render(request,"profil_content.html", {'user': user})

    elif num == 10:
        ListUser = User.objects.all()
        Ladderlist = [user] * 18
        test = [user] * len(ListUser)
        
        j = 0
        while j < len(ListUser):
            test[j] = ListUser[j]           #create a usable list
            j = j + 1
        
        Void = User(idUser=0, idType=0, username="", profilPicture="images/default/void.png", tokenJWT="", money=0, idStatus=0)

        j = 0
        while j < 18 and len(test) != 0:            #keeping only the 18 best
            i = 1
            whoUser = 0
            user = test[0]
            while i < len(test):
                if test[i].money > user.money:
                    user = test[i]
                    whoUser = i
                i = i + 1
            Ladderlist[j] = user
            test.pop(whoUser)
            j = j + 1
        while j < 18:
            Ladderlist[j] = Void
            j = j + 1
        if fullPage:
            return render(request, "ladder_full.html", {'Ladderlist': Ladderlist})
        else:
            return render(request,"ladder.html", {'Ladderlist': Ladderlist})

    elif num == 11:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            if not "/default/" in user.profilPicture.name:
                file = "./media/" + user.profilPicture.name
                os.remove(file)
            data= form.cleaned_data.get("profilPicture")
            user.profilPicture = data
            user.save()
            return render(request, "toProfile.html")
        if fullPage:
            return render(request, "changeProfilePicture_full.html", {"form":UserForm(request.POST, request.FILES)})
        else:
            return render(request,"changeProfilePicture.html", {"form":UserForm(request.POST, request.FILES)})

    else:
        if fullPage:
            return render(request, "index.html")
        else:
            return render(request, "index_spa.html")


def gamePage(request):
    return render(request,"game.html")
