# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2024/01/08 16:16:40 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hashlib, jwt, sys
import backend.settings as settings

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from db_test.models import User
from db_test.models import Status
from db_test.models import connectionPassword

# **************************************************************************** #
#                                Check Functions                               #
# **************************************************************************** #
@csrf_exempt
def checkLogin(request):
    username = request.POST.get('login')
    password = request.POST.get('password')

    username_check = User.objects.all().filter(username=username)
    if len(username_check) == 0:
        return JsonResponse({"success" : False, "error" : "Username not exist"})

    password_check = connectionPassword.objects.all().filter(idUser=username_check[0].idUser)
    if len(password_check) == 0:
        return JsonResponse({"success" : False, "error" : "No password authentification"})

    hash = hashlib.sha512(password.encode(), usedforsecurity=True)
    if hash.hexdigest() != password_check[0].password:
        return JsonResponse({"success" : False, "error" : "Password incorrect"})

    token = jwt.encode({"userId": username_check[0].idUser}, settings.SECRET_KEY, algorithm="HS256")

    #username_check[0].tokenJWT = token
    #User.save()

    return JsonResponse({"success" : True, "token" : token})


@csrf_exempt
def checkSignin(request):
    username = request.POST.get('login2')
    password = request.POST.get('password2')
    passwordconfirm = request.POST.get('confirm')

    if not username or password == "" or passwordconfirm == "":
        return JsonResponse({"success" : False, "error" : "Empty field aren't accept"})

    test = User.objects.all().filter(username=username)
    if len(test):
        return JsonResponse({"success" : False, "error" : "Username already use"})

    if password != passwordconfirm:
        return JsonResponse({"success" : False, "error" : "Password and confirm aren't the same"})

    hashPwd = hashlib.sha512(password.encode(), usedforsecurity=True)

    id = User.objects.all().count() + 1
    idType = 1

    try:
        status= Status(idStatus='0', name="On")
        status.save()
    except:
        return JsonResponse({"success" : False, "error" : "Error on status creation"})

    token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
    try:
        user = User(idUser=id, idType=idType, username=username, profilPicture="NULL", tokenJWT=token, money=0, idStatus=Status.objects.get(idStatus=0))
        user.save()
    except:
        return JsonResponse({"success" : False, "error" : "Error on user creation"})

    try:
        password = connectionPassword(idPassword=id, password=hashPwd.hexdigest(), idUser=user)
        password.save()
    except:
        return JsonResponse({"success" : False, "error" : "Error on password creation"})

    return JsonResponse({"success" : True, "token" : token})


@csrf_exempt
def checkToken(request):
    token = request.COOKIES.get('token', None)

    if token == None or token == "undefined":
        return {"success" : False, "error" : "No token send"}

    data = None
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    except Exception as error:
        return {"success" : False, "error" : "Token undecodable - " + str(error)}

    userId = data["userId"]
    users = User.objects.all().filter(idUser=userId)
    if len(users) == 0:
        return {"success" : False, "error" : "User id invalid"}
    if len(users) > 1:
        return {"success" : False, "error" : "User id duplicate"}

    if users[0].tokenJWT != token:
        return {"success" : False, "error" : "Invalid token"}

    return {"success" : True, "userId" : userId}


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
    user = User.objects.all().filter(idUser=userId)[0]

    htmlText = render(request,"navbar.html", {'user': user}).getvalue().decode()
    return JsonResponse({"success" : True, "html" : htmlText})


@csrf_exempt
def section(request, num):
    """_summary_

    Args:
        request (_type_): The request
        num (_type_): Which page to load

    Raises:
        Http404: When the num is incorrect

    Returns:
        _type_: The page to render
    """
    if num == 0:
        return render(request, "index_spa.html")

    elif num == 1:
        return render(request, "signin.html")

    elif num == 2:
        return render(request, "login.html")

    # Check token
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    # Get the user
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]

    if num == 3:
        return render(request, "mainpage.html")

    elif num == 4:
        return render(request,"waitpage.html")

    elif num == 5:
        return render(request,"createGameRoom.html")

    elif num == 6:
        return render(request,"game.html")

    elif num == 7:
        return render(request,"tournament.html")

    elif num == 8:
        return render(request,"tournamentcreate.html")

    elif num == 9:
        return render(request,"profil_content.html")

    elif num == 10:
        return render(request,"ladder.html")

    else:
        raise Http404("Section doesn't exist")
