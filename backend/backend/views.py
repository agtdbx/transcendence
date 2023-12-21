# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/12/21 16:09:02 by aderouba         ###   ########.fr        #
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
def checkLogin(request):
    username = request.POST.get('login')
    password = request.POST.get('password')

    username_check = User.objects.all().filter(username=username)
    if len(username_check) == 0:
        return {"success" : False, "error" : "Username not exist"}

    password_check = connectionPassword.objects.all().filter(idUser=username_check[0].idUser)
    if len(password_check) == 0:
        return {"success" : False, "error" : "No password authentification"}

    hash = hashlib.sha512(password.encode(), usedforsecurity=True)
    if hash.hexdigest() != password_check[0].password:
        return {"success" : False, "error" : "Password incorrect"}

    token = jwt.encode({"userId": username_check[0].idUser}, settings.SECRET_KEY, algorithm="HS256")

    #username_check[0].tokenJWT = token
    #User.save()

    return {"success" : True, "token" : token}


def checkSignin(request):
    username = request.POST.get('login2')
    password = request.POST.get('password2')
    passwordconfirm = request.POST.get('confirm')

    if not username or password == "" or passwordconfirm == "":
        return {"success" : False, "error" : "Empty field aren't accept"}

    test = User.objects.all().filter(username=username)
    if len(test):
        return {"success" : False, "error" : "Username already use"}

    if password != passwordconfirm:
        return {"success" : False, "error" : "Password and confirm aren't the same"}

    hashPwd = hashlib.sha512(password.encode(), usedforsecurity=True)

    id = User.objects.all().count() + 1
    idType = 1

    try:
        status= Status(idStatus='0', name="On")
        status.save()
    except:
        return {"success" : False, "error" : "Error on status creation"}

    token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
    try:
        user = User(idUser=id, idType=idType, username=username, profilPicture="NULL", tokenJWT=token, money=0, idStatus=Status.objects.get(idStatus=0))
        user.save()
    except:
        return {"success" : False, "error" : "Error on user creation"}

    try:
        password = connectionPassword(idPassword=id, password=hashPwd.hexdigest(), idUser=user)
        password.save()
    except:
        return {"success" : False, "error" : "Error on password creation"}

    return {"success" : True, "token" : token}


def checkToken(request):
    token = request.COOKIES.get('token', None)

    if token == None:
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
def section(request, num):
    if num == 1: # Page d'accueil
        check = checkLogin(request)
        if check["success"] == False:
            return JsonResponse(check)
        htmlText = render(request,"mainpage.html").getvalue().decode()
        return JsonResponse({"success" : True, "html" : htmlText, "token" : check["token"]})

    elif num == 2: # Page de connexion
        check = checkSignin(request)
        if check["success"] == False:
            return JsonResponse(check)
        htmlText = render(request,"mainpage.html").getvalue().decode()
        return JsonResponse({"success" : True, "html" : htmlText, "token" : check["token"]})

    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]

    if num == 0:
        user = User.objects.all().filter(idUser=userId)
        htmlText = render(request,"navbar.html", {'user': user[0] }).getvalue().decode()
        return JsonResponse({"success" : True, "html" : htmlText})

    elif num == 3:# Page de création de compte
        htmlText = render(request,"mainpage.html").getvalue().decode()
        return JsonResponse({"success" : True, "html" : htmlText})

    elif num == 4:
        htmlText = render(request,"waitpage.html").getvalue().decode()
        res = JsonResponse({"success" : True, "html" : htmlText})
        return res

    elif num == 5:
        htmlText = render(request,"createGameRoom.html").getvalue().decode()
        return JsonResponse({"success" : True, "html" : htmlText})

    elif num == 6:
        htmlText = render(request,"tournament.html").getvalue().decode()
        return JsonResponse({"success" : True, "html" : htmlText})

    elif num == 7:
        htmlText = render(request,"profil_content.html").getvalue().decode()
        return JsonResponse({"success" : True, "html" : htmlText})

    elif num == 8:
        htmlText = render(request,"index.html").getvalue().decode()
        return JsonResponse({"success" : True, "html" : htmlText})

    else:
        return JsonResponse({"success" : False, "error" : "Section doesn't exist"})


