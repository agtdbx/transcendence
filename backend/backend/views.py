# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/12/18 18:35:22 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hashlib, jwt, sys
import backend.settings as settings

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


from db_test.models import User
from db_test.models import Status
from db_test.models import connectionPassword


# Create check JWT Token
class LoginView(APIView):
    def post(sefl, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        })


# def testJS(request):
#     return render(request,"other.html")

@csrf_exempt
def testPY(request):

    return HttpResponse("success")


def index(request):
    return render(request, 'index.html')

randomstring = ["This is section 1.","This is section 2.", "This is section 3."]


def checkLogin(request):
    if request.method != 'POST':
        return JsonResponse({"success" : False, "error" : "Get access refused"})

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

    return JsonResponse({"success" : True, "token" : token})


def checkSignin(request):
    if request.method != 'POST':
        return JsonResponse({"success" : False, "error" : "Get access refused"})

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


def section(request, num):
    if num == 0:
        user = User.objects.all()
        return render(request,"navbar.html", {'user': user[0] })

    if request.method != 'POST':
        return HttpResponse("Get access refused")

    if num == 1: # Page d'accueil
        return render(request,"mainpage.html")
    elif num == 2: # Page de connexion
        return render(request,"mainpage.html")
    elif num == 3:# Page de création de compte
        return render(request,"mainpage.html")
    elif num == 4:
        return render(request,"waitpage.html")
    elif num == 5:
        return render(request,"createGameRoom.html")
    elif num == 6:
        return render(request,"tournament.html")
    elif num == 7:
        return render(request,"profil_content.html")
    elif num == 8:
        return render(request,"index.html")
    else:
        raise Http404('No such section')

    # if num == 0:
    #     user = User.objects.all()
    #     return JsonResponse({"success" : True, "html" : render(request,"navbar.html", {'user': user[0] })})

    # if request.method != 'POST':
    #     return JsonResponse({"success" : False, "error" : "Get access refused"})

    # htmlText = ""

    # if num == 1: # Page d'accueil
    #     htmlText = render(request,"mainpage.html")
    # elif num == 2: # Page de connexion
    #     htmlText = render(request,"mainpage.html")
    # elif num == 3:# Page de création de compte
    #     htmlText = render(request,"mainpage.html")
    # elif num == 4:
    #     htmlText = render(request,"waitpage.html")
    # elif num == 5:
    #     htmlText = render(request,"createGameRoom.html")
    # elif num == 6:
    #     htmlText = render(request,"tournament.html")
    # elif num == 7:
    #     htmlText = render(request,"profil_content.html")
    # elif num == 8:
    #     htmlText = render(request,"index.html")
    # else:
    #     return JsonResponse({"success" : False, "error" : "Section does'nt exist"})
    #     # raise Http404('No such section')

    # return JsonResponse({"success" : True, "html" : htmlText})
