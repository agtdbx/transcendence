# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2024/01/17 14:12:00 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hashlib, jwt, sys
import backend.settings as settings

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render

from db_test.models import User, connectionPassword, Message, Link
import datetime

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

    token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
    try:
        #the image are in /backend/media/...
        #add random for profile picture
        user = User(idUser=id, idType=idType, username=username, profilPicture="images/default/Scout.png", tokenJWT=token, money=0, idStatus=0)
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
def otherProfilPage(request, pseudo):
    check = checkToken(request)
    if check["success"] == False:
        return render(request, "index.html")
    try :
        user = User.objects.all().filter(username=pseudo)[0]
        fullPage = (request.method != 'POST')
        if fullPage:
            return render(request, "other_profil_content_full.html", {'user': user})
        else:
            return render(request,"other_profil_content.html", {'user': user})
    except :
        return render(request, "gamePage.html")


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


# **************************************************************************** #
#                            DB connexion Functions                            #
# **************************************************************************** #
@csrf_exempt
def sendMessage(request):
    if request.method != 'POST':
        return JsonResponse({"success" : False, "error" : "Only post accepted"})

     # Check token
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    # Get the user
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    idMsg = len(Message.objects.all())
    data = request.POST.get("message")
    date = datetime.datetime.now()
    try:
        msg = Message.objects.create(id=idMsg, idUser=user, date=date, data=data)
        msg.save()
    except Exception as error:
        return JsonResponse({"success" : False, "error" : "Can't create the message : " + str(error)})

    return JsonResponse({"success" : True})


def getMessages(request):
    pass


# **************************************************************************** #
#                            Users Relations Functions                         #
# **************************************************************************** #

def haveRelation(user, target):
    """
    return True if user and target have a relation, else, return False
    """
    return (len(Link.objects.all().filter(idUser=user.idUser, idTarget=target.idUser)) > 0)

def getTarget(targetName):
    """
    return the user object in db who have targetName as username, if there is not user with this username, return None
    """
    targetListe = User.objects.all().filter(username=targetName)
    if len(targetListe) > 0:
        return targetListe[0]
    return None

def createRelation(user, target):
    """
    create a Link in db between user and target return True if the db request success, false in the other case
    """
    id = Link.objects.all().count()

    if user.idUser == target.idUser:
        return False

    try:
        #the image are in /backend/media/...
        #add random for profile picture
        link = Link(idUser=user, idTarget=target.idUser, id=id, link=0)
        link.save()
        return True
    except:
        return False

#TODO end this :

def addfriends(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    if not haveRelation(user, target):
        if not createRelation(user, target) :
            return JsonResponse({"success": False, "content" : "Error : creation of user relation." })
    try :
        link = Link.objects.all().filter(idUser=user.idUser, idTarget=target.idUser)[0]
        if link.link == 2:
            return JsonResponse({"success": False, "content" : "You can't send a friend request to " + request.POST.get('friend') +"." })
        link.link = 1
        link.save()
    except :
         return JsonResponse({"success": False, "content" : "Error : modification of user relation." })

    return JsonResponse({"success": True, "content" : "request send to " + request.POST.get('friend') +"." })


def removefriends(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    if not haveRelation(user, target) or not haveRelation(target, user):
        return JsonResponse({"success": False, "content" : "Error : You're not friends" })
    try :
        link1 = Link.objects.all().filter(idUser=user.idUser, idTarget=target.idUser)[0]
        link2 = Link.objects.all().filter(idUser=target.idUser, idTarget=user.idUser)[0]
        link1.link = 0
        link2.link = 0
        link1.save()
        link2.save()		
    except :
         return JsonResponse({"success": False, "content" : "Error : modification of user relation." })

    return JsonResponse({"success": True, "content" : "request send to " + request.POST.get('friend') +"." })


def acceptfriends(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    if not haveRelation(target, user) or Link.objects.all().filter(idUser=target.idUser, idTarget=user.idUser)[0].link != 1:
        return JsonResponse({"success": False, "content" : "Error : You haven't received a friend request." })
    if not haveRelation(user, target):
        if not createRelation(user, target) :
            return JsonResponse({"success": False, "content" : "Error : creation of user relation." })
    try :
        link1 = Link.objects.all().filter(idUser=user.idUser, idTarget=target.idUser)[0]
        link2 = Link.objects.all().filter(idUser=target.idUser, idTarget=user.idUser)[0]
        link1.link = 2
        link2.link = 2
        link1.save()
        link2.save()
    except :
         return JsonResponse({"success": False, "content" : "Error : modification of user relation." })

    return JsonResponse({"success": True, "content" : "request of " + request.POST.get('friend') +" accepted." })

	
def refusefriends(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    if not haveRelation(target, user) or Link.objects.all().filter(idUser=target.idUser, idTarget=user.idUser)[0].link != 1:
        return JsonResponse({"success": False, "content" : "Error : You haven't received a friend request." })

    try :
        link = Link.objects.all().filter(idUser=target.idUser, idTarget=user.idUser)[0]
        link.link = 0
        link.save()
    except :
         return JsonResponse({"success": False, "content" : "Error : modification of user relation." })

    return JsonResponse({"success": True, "content" : "request of " + request.POST.get('friend') +" refused." })


def block(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    if not haveRelation(user, target):
        if not createRelation(user, target) :
            return JsonResponse({"success": False, "content" : "Error : creation of user relation." })
    try :
        link1 = Link.objects.all().filter(idUser=user.idUser, idTarget=target.idUser)[0]
        link1.link = 3
        link1.save()
        if haveRelation(target, user) and Link.objects.all().filter(idUser=target.idUser, idTarget=user.idUser)[0].link == 2:
            link2 = Link.objects.all().filter(idUser=target.idUser, idTarget=user.idUser)[0]
            link2.link = 0
            link2.save()		
    except :
         return JsonResponse({"success": False, "content" : "Error : modification of user relation." })

    return JsonResponse({"success": True, "content" : "request send to " + request.POST.get('friend') +"." })


def unblock(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user." })
    if not haveRelation(user, target):
        return JsonResponse({"success": False, "content" : "Error : " + request.POST.get('friend') + " wasn't blocked." })
    try :
        link = Link.objects.all().filter(idUser=user.idUser, idTarget=target.idUser)[0]
        if link.link != 3:
            return JsonResponse({"success": False, "content" : "You can't unblocked " + request.POST.get('friend') +"." })
        link.link = 0
        link.save()
    except :
         return JsonResponse({"success": False, "content" : "Error : modification of user relation." })

    return JsonResponse({"success": True, "content" : "unblocked : " + request.POST.get('friend') })


def getrelation(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    target = getTarget(request.POST.get('friend'))
    if target == None:
        return JsonResponse({"success": False, "content" : "Inexistant user.", "value" : None })
    if not haveRelation(user, target):
        return JsonResponse({"success": True, "content" : "", "value" : 0 })
    linkType = Link.objects.all().filter(idUser=user.idUser, idTarget=target.idUser)[0].link
    return JsonResponse({"success": True, "content" : "", "value" : linkType })

def getlistefriendrequest(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    linkFriendRequestList = Link.objects.all().filter(idTarget=user.idUser, link=1)
    listeRequest = []
    for link in linkFriendRequestList :
        try:
            sender = User.objects.all().filter(link=link)[0]
            if haveRelation(user, sender) and len(Link.objects.all().filter(idUser=user.idUser, idTarget=sender.idUser, link=3)) > 0:
                continue      
            listeRequest.append(sender.username)
        except:
            continue
    return JsonResponse({"success": True, "content" : "", "listRequest" : listeRequest })

def getlistefriend(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    linkFriendRequestList = Link.objects.all().filter(idUser=user.idUser, link=2)
    listeRequest = []
    for link in linkFriendRequestList :
        try:
            friend = User.objects.all().filter(link=link)[0] 
            listeRequest.append({"name": friend.username, "pp" : "./media/" + friend.profilPicture.name, "status" : friend.idStatus })
        except:
            continue
    return JsonResponse({"success": True, "content" : "", "listcontact" : listeRequest })

def getlisteblocked(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    linkFriendRequestList = Link.objects.all().filter(idUser=user.idUser, link=3)
    listeRequest = []
    for link in linkFriendRequestList :
        try:
            friend = User.objects.all().filter(link=link)[0] 
            listeRequest.append({"name": friend.username, "pp" : "./media/" + friend.profilPicture.name, "status" : friend.idStatus })
        except:
            continue
    return JsonResponse({"success": True, "content" : "", "listcontact" : listeRequest })