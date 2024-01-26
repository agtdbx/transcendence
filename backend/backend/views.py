# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2024/01/26 16:54:33 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from db_test.models import User

from .forms import UserForm

from .views_connection import checkToken


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
        if fullPage:
            return render(request, "profil_content_full.html", {'user': user})
        else:
            return render(request,"profil_content.html", {'user': user})

    elif num == 10:
        if fullPage:
            return render(request, "ladder_full.html")
        else:
            return render(request,"ladder.html")

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
