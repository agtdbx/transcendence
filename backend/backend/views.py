# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2024/01/16 15:31:20 by hde-min          ###   ########.fr        #
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

from .forms import UserForm

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
        #the image are in /backend/media/...
        #add random for profile picture
        user = User(idUser=id, idType=idType, username=username, profilPicture="images/default/Scout.png", tokenJWT=token, money=0, idStatus=Status.objects.get(idStatus=0))
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
            return render(request, "profil_content_full.html")
        else:
            return render(request,"profil_content.html")

    elif num == 10:
        if fullPage:
            return render(request, "ladder_full.html")
        else:
            return render(request,"ladder.html")
        
    elif num == 11:
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            data= form.cleaned_data.get("profilPicture")
            user.profilPicture = data
            user.save()
            #return (section(request, 9))
            #num should be = to 9 but its not, need to fix it
            #return render(request, "profil_content_full.html")
        if fullPage:
            return render(request, "changeProfilePicture.html", {"form":UserForm(request.POST, request.FILES)})
        else:
            return render(request,"changeProfilePicture.html", {"form":UserForm(request.POST, request.FILES)})

    else:
        if fullPage:
            return render(request, "index.html")
        else:
            return render(request, "index_spa.html")


def UserProfilPic(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        idUser = request.POST.get('password')
        idType = idUser

        # Create a new patient entry in the database using the Patient model

        status= Status(idStatus='0', name="Online")
        status.save()

        user = User(idUser=idUser, idType=idType, username=username, profilPicture="wrgsd", tokenJWT="wgdsv", money=1, idStatus=Status(idStatus='0', name="Online"))
        user.save()



        return render(request,"mainpage.html")
    else:
        return HttpResponse("Invalid request method.")

def gamePage(request):
	return render(request,"game.html")
