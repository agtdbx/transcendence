# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_connection.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/23 19:48:51 by aderouba          #+#    #+#              #
#    Updated: 2024/02/19 18:00:45 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# **************************************************************************** #
#                                Check Functions                               #
# **************************************************************************** #
import hashlib, jwt, random, os
import backend.settings as settings
import requests
import datetime

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from db_test.models import User, connectionPassword, connection42, Link
from django.shortcuts import render
from django.contrib import messages


def generateToken(id:int) -> str:
    jwtCreation = datetime.datetime.now()
    jwtTimeout = jwtCreation + datetime.timedelta(days=5)

    token = jwt.encode({"userId": id,
                        "creation" : jwtCreation.strftime("%d/%m/%Y %H:%M:%S"),
                        "timeout" : jwtTimeout.strftime("%d/%m/%Y %H:%M:%S")}
                       , settings.SECRET_KEY, algorithm="HS256")
    return token


def checkToken(request):
    token = request.COOKIES.get('token', None)

    if token == None or token == "undefined":
        return {"success" : False, "error" : "No token send"}

    data = None
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    except Exception as error:
        return {"success" : False, "error" : "Token undecodable - " + str(error)}

    userId = data.get("userId", None)
    creationStr = data.get("creation", None)
    timeoutStr = data.get("timeout", None)

    if userId == None or creationStr == None or timeoutStr == None:
        return {"success" : False, "error" : "Token invalid"}

    now = datetime.datetime.now()
    creation = datetime.datetime.strptime(creationStr, '%d/%m/%Y %H:%M:%S')
    timeout = datetime.datetime.strptime(timeoutStr, '%d/%m/%Y %H:%M:%S')

    if creation > now:
        return {"success" : False, "error" : "Creation token invalid"}

    if timeout <= now:
        return {"success" : False, "error" : "Token timeout"}

    users = User.objects.all().filter(idUser=userId)
    if len(users) == 0:
        return {"success" : False, "error" : "User id invalid"}
    if len(users) > 1:
        return {"success" : False, "error" : "User id duplicate"}

    return {"success" : True, "userId" : userId}


@csrf_exempt
def checkLogin(request):
    if request.method != 'POST':
        return JsonResponse({"success" : False, "error" : "Only post request"})

    username = request.POST.get('login')
    password = request.POST.get('password')

    # Check if username haven't bad caracters
    username = username.lower()
    good_chars = "abcdefghijklmnoprstuvwxyz0123456789_"
    for c in username:
        if c not in good_chars:
            return JsonResponse({"success" : False, "error" : "Only alphanum and underscore autorised"})

    username_check = User.objects.all().filter(username=username)
    if len(username_check) == 0:
        return JsonResponse({"success" : False,
                             "error" : "Username does not exist"})

    password_check = connectionPassword.objects.all()\
                        .filter(idUser=username_check[0].idUser)
    if len(password_check) == 0:
        return JsonResponse({"success" : False,
                             "error" : "No password authentification"})

    hash = hashlib.sha512(password.encode(), usedforsecurity=True)
    if hash.hexdigest() != password_check[0].password:
        return JsonResponse({"success" : False, "error" : "Password incorrect"})
    token = generateToken(username_check[0].idUser)

    return JsonResponse({"success" : True, "token" : token})


@csrf_exempt
def checkSignin(request):
    if request.method != 'POST':
        return JsonResponse({"success" : False, "error" : "Only post request"})

    username = request.POST.get('login2')
    password = request.POST.get('password2')
    passwordconfirm = request.POST.get('confirm')

    if not username or password == "" or passwordconfirm == "":
        return JsonResponse({"success" : False,
                             "error" : "Empty field aren't accept"})

    if len(username) == 0:
        return JsonResponse({"success" : False, "error" : "new name can't be empty"})

    elif len(username) > 10:
        return JsonResponse({"success" : False, "error" : "new name too long (max 10)"})

    # Check if username haven't bad caracters
    username = username.lower()
    good_chars = "abcdefghijklmnopqrstuvwxyz0123456789_-"
    for c in username:
        if c not in good_chars:
            return JsonResponse({"success" : False, "error" : "Only alphanum and underscore autorised"})

    test = User.objects.all().filter(username=username)
    if len(test):
        return JsonResponse({"success" : False, "error" : "Username already use"})

    if password != passwordconfirm:
        return JsonResponse({"success" : False,
                             "error" : "Password and confirm aren't the same"})

    hashPwd = hashlib.sha512(password.encode(), usedforsecurity=True)

    id = User.objects.all().count() - 1
    idType = 1

    token = generateToken(id)
    try:
        str = ["images/default/Scout.png", "images/default/Driller.png",
               "images/default/Engineer.png", "images/default/Soldier.png"]
        user = User(idUser=id, type=idType, username=username,
                    profilPicture=str[random.randint(0,3)],
                    money=10, status=0)
        user.save()
    except:
        return JsonResponse({"success" : False,
                             "error" : "Error on user creation"})

    try:
        password = connectionPassword(idPassword=id, password=hashPwd.hexdigest(),
                                      idUser=user)
        password.save()
    except:
        return JsonResponse({"success" : False,
                             "error" : "Error on password creation"})

    try:
        idLink = Link.objects.all().count()

        link = Link.objects.create(id=idLink, idUser=user, idTarget=0, link=2)
        link.save()

    except:
        return JsonResponse({"success" : False,
                             "error" : "Error on link creation"})
    return JsonResponse({"success" : True, "token" : token})


@csrf_exempt
def changePassword(request):
    if request.method != 'POST':
        return JsonResponse({"success" : False, "error" : "Only post request"})

    currentPassword = request.POST.get('currentPass')
    newPassword = request.POST.get('newPass')
    newPasswordComfirm = request.POST.get('newPassConfirm')
    check = checkToken(request)
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]

    password_check = connectionPassword.objects.all().filter(idUser=user.idUser)
    if (len(password_check) != 0): #if user has a password
        password_check = password_check[0]
        hash = hashlib.sha512(currentPassword.encode(), usedforsecurity=True)
        if hash.hexdigest() != password_check.password:
            return JsonResponse({"success" : False, "error" :
                                    "Wrong account password, please try again !"})
    else :            #if user hasn't a password
        password_check = connectionPassword(idPassword=user.idUser, password="",
                                            idUser=user)
    if newPassword != newPasswordComfirm:
        return JsonResponse({"success" : False, "error" :
                                "New password is different from new password " +
                                "confirmation, please try again !"})
    else:
        hashPwd = hashlib.sha512(newPassword.encode(), usedforsecurity=True)
        try:
            hashPwd = hashlib.sha512(newPassword.encode(), usedforsecurity=True)
            password_check.password = hashPwd.hexdigest()
            password_check.save()
        except:
            return JsonResponse({"success" : False,
                                 "error" : "Somethink very wrong appened, please "
                                 + "try again !"})
    return JsonResponse({"success" : True})


@csrf_exempt
def changeUsername(request):
    if request.method != 'POST':
        return JsonResponse({"success" : False, "error" : "Only post request"})

    newName = request.POST.get('newName', None)

    if newName == None:
        return JsonResponse({"success" : False, "error" : "Missing new name"})

    if len(newName) == 0:
        return JsonResponse({"success" : False, "error" : "new name can't be empty"})

    elif len(newName) > 10:
        return JsonResponse({"success" : False, "error" : "new name too long (max 10)"})

    # Check if newName haven't bad caracters
    newName = newName.lower()
    good_chars = "abcdefghijklmnopqrstuvwxyz0123456789_-"
    for c in newName:
        if c not in good_chars:
            return JsonResponse({"success" : False, "error" : "Only alphanum and underscore autorised"})


    check = checkToken(request)
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    user1 = User.objects.all()

    i = 0
    while i < len(user1):
        if user1[i].username == newName:
            if user1[i].idUser != userId:
                return JsonResponse({"success" : False,
                                     "error" : "This Username is already taken !"})
        i = i + 1
    if newName == user.username:
        return JsonResponse({"success" : False,
                             "error" : "This is already your Username !"})
    else:
        try:
            user.username = newName
            user.save()
        except:
            return JsonResponse({"success" : False,
                                 "error" : "Somethink very wrong appened, please "
                                 + "try again !"})
        return JsonResponse({"success" : True})


def checkApi42Request(request, islogin, user:User):
    code = request.GET.get('code')
    # First request : get an users tocken
    i = 1
    j = 0
    if not islogin :
        ListUser = User.objects.all()
        while j < len(ListUser):
            if user.money < ListUser[j].money:
                i = i + 1
            j = j + 1
    websiteUrl = os.getenv('WEBSITE_URL')
    params = \
    {
        "grant_type": "authorization_code",
        "client_id": "u-s4t2ud-1b900294f4f0042d646cdbafdf98a5fe9216f3ef" +
                     "d76b592e56b7ae3a18a43bd1",
        "client_secret": os.getenv('API_KEY'),
        "code": code,
        "redirect_uri": websiteUrl + "/3" if islogin else websiteUrl + "/9",

    }
    response = requests.post("https://api.intra.42.fr/oauth/token", params=params)
    if response.status_code != 200:
        if not islogin :
            return render(request, "profil_content_full.html",
                          {'user': user, 'pos': i,
                           '42urllink' : os.getenv('WEBSITE_URL')})
        else :
            return render(request, "signin_full.html",
                          {'42urllink' : os.getenv('WEBSITE_URL')})
    response = response.json()
    tocken = response["access_token"]
    headers= {'Authorization': 'Bearer {}'.format(tocken)}
    response = requests.get("https://api.intra.42.fr/v2/me", headers=headers)
    if response.status_code != 200:
        if not islogin :
            return render(request, "profil_content_full.html",
                          {'user': user, 'pos': i,
                           '42urllink' : os.getenv('WEBSITE_URL')})
        else :
            return render(request, "signin_full.html",
                          {'42urllink' : os.getenv('WEBSITE_URL')})
    response = response.json()
    test = connection42.objects.all().filter(login=response["id"])
    if (not islogin) :
        if len(test) == 0:
            try :
                password42 = connection42(login=response["id"], idUser=user)
                password42.save()
            except:
                user = user
        return render(request, "profil_content_full.html",
                      {'user': user, 'pos': i,
                       '42urllink' : os.getenv('WEBSITE_URL')})

    #not already log
    if len(test) == 0:
        id = User.objects.all().count() - 1
        idType = 1

        # token = generateToken(id)
        username = response["login"]
        number = 0
        while User.objects.all().filter(username=username):
            username = response["login"] + str(number)
            number+=1
            if number > 99 :
                response["login"] = ""
        try:
            imgpath = ["images/default/Scout.png", "images/default/Driller.png",
                       "images/default/Engineer.png", "images/default/Soldier.png"]
            user = User(idUser=id, type=idType, username=username,
                        profilPicture=imgpath[random.randint(0,3)],
                        money=10, status=0)
            user.save()
            password42 = connection42(login=response["id"], idUser=user)
            password42.save()
        except:
            return render(request, "login_full.html",
                          {'42urllink' : os.getenv('WEBSITE_URL')})
        return render(request, "mainpage_full_tocken42.html", {'idType': user.type, 'token' : generateToken(user.idUser)})

    #already log
    else:
        try:
            user = User.objects.all().filter(connection42=test[0])[0]
        except:
            return render(request, "login_full.html",
                          {'42urllink' : os.getenv('WEBSITE_URL')})
        return render(request, "mainpage_full_tocken42.html", {'idType': user.type, 'token' : generateToken(user.idUser)})
