# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2024/02/08 13:47:07 by hde-min          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import  os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from db_test.models import UserTournament
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


def apiDoc(request):
    return render(request, 'api_doc.html')


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

    ListUser = User.objects.all()
    i = 1
    j = 0
    while j < len(ListUser):                               #take rank
        if user.money < ListUser[j].money:
            i = i + 1
        j = j + 1
    pp = "./image/ladder/rock-and-pong-rank" + str(i - 1) + ".png"
    htmlText = render(request,"navbar.html", {'user': user, 'rank': i, 'rankpicture': pp}).getvalue().decode()
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
            return render(request, "signin_full.html",{'42urllink' : os.getenv('WEBSITE_URL')})
        else:
            return render(request, "signin.html",{'42urllink' : os.getenv('WEBSITE_URL')})

    elif num == 2:
        if fullPage:
            return render(request, "login_full.html",{'42urllink' : os.getenv('WEBSITE_URL')})
        else:
            return render(request, "login.html",{'42urllink' : os.getenv('WEBSITE_URL')})

    #conecting with 42 api
    elif num == 3 and fullPage and request.GET.get('code', None) != None:
        return checkApi42Request(request, True, None)


    # Check token
    check = checkToken(request)
    if check["success"] == False:
        if fullPage:
            return render(request, "login_full.html",{'42urllink' : os.getenv('WEBSITE_URL')})
        else:
            return render(request, "login.html",{'42urllink' : os.getenv('WEBSITE_URL')})

    # Get the user
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]

    if num == 3:
        if fullPage:
            return render(request, "mainpage_full.html", {'idType': user.idType})
        else:
            return render(request, "mainpage.html", {'idType': user.idType})

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

    elif num == 7:   #do nothing problably best to kill it
        if fullPage:
            return render(request, "tournament_full.html")
        else:
            return render(request,"tournament.html")

    elif num == 8: #admin page where you can create tournament if you are admin and start them
        if(user.idType != 2):
            return render(request, "mainpage_full.html")
        if fullPage:
            return render(request, "tournament_full.html")
        else:
            return render(request,"tournament.html")

    elif num == 9:
        ListUser = User.objects.all()
        i = 1
        j = 0
        while j < len(ListUser):
            if user.money < ListUser[j].money:
                i = i + 1
            j = j + 1
        if fullPage and request.GET.get('code', None) != None:
            return checkApi42Request(request, False, user)
        elif fullPage :
            return render(request, "profil_content_full.html", {'user': user, 'pos': i, '42urllink' : os.getenv('WEBSITE_URL')})
        else:
            return render(request,"profil_content.html", {'user': user, 'pos': i, '42urllink' : os.getenv('WEBSITE_URL')})

    elif num == 10:
        ListUser = list(User.objects.all().order_by("-money"))
        ListUser = ListUser[:18]

        Void = User(idUser=0, idType=0, username="", profilPicture="images/default/void.png", tokenJWT="", money=0, idStatus=0)

        j = len(ListUser)
        while j < 18:
            ListUser.append(Void)
            j += 1
        i = 0
        j = 0
        while j < 18:                                           #check if user is in the list
            if user.username == ListUser[j].username:
                i = -1
            j = j + 1

        if i != -1:                                             #if user not in list add him in spot 18
            ListUser[17] = user
            ListUser2 = User.objects.all()
            i = 1
            j = 0
            while j < len(ListUser2):                               #if user is in the list we need is rank
                if user.money < ListUser2[j].money:
                    i = i + 1
                j = j + 1
        else:
            i = 18
        if fullPage:
            return render(request, "ladder_full.html", {'Ladderlist': ListUser, 'pos': i})
        else:
            return render(request,"ladder.html", {'Ladderlist': ListUser, 'pos': i})

    elif num == 11:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            if not "/default/" in user.profilPicture.name:
                file = "./media/" + user.profilPicture.name
                if os.path.isfile(file):
                    os.remove(file)
            data= form.cleaned_data.get("profilPicture")
            user.profilPicture = data
            user.save()
            return render(request, "toProfile.html")
        if fullPage:
            return render(request, "changeProfilePicture_full.html", {"form":UserForm(request.POST, request.FILES)})
        else:
            return render(request,"changeProfilePicture.html", {"form":UserForm(request.POST, request.FILES)})
    elif num == 12:
        if fullPage:
            return render(request, "beer_full.html")
        else:
            return render(request,"beer.html")
        
    elif num == 13:                 # inscription page
        #need to register USER and check if tournament is full or not
        #save user
        if fullPage:
            return render(request, "joinTournament_full.html")
        else:
            return render(request,"joinTournament.html")
        
    elif num == 14: #check if user is register or if tournament is full if not register
        if UserTournament.objects.all().filter(idUser=user.idUser):     #already join tournament
            if fullPage:        
                return render(request, "joinTournament_full.html")
            else:
                return render(request,"joinTournament.html")
        if len(UserTournament.objects.all()) == 8:  #tournament full -> join spectate
            if fullPage:
                return render(request, "tournamentSpectate_full.html")
            else:
                return render(request,"tournamentSpectate.html")
        else:
            if fullPage:
                return render(request, "tournamentInscription_full.html")   #subscribe to tournament
            else:
                return render(request,"tournamentInscription.html")

    else:
        if fullPage:
            return render(request, "index.html")
        else:
            return render(request, "index_spa.html")


def gamePage(request):
    return render(request,"game.html")
