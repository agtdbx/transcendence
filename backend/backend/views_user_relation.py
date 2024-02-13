# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_user_relation.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/23 19:48:59 by aderouba          #+#    #+#              #
#    Updated: 2024/02/10 17:22:21 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# **************************************************************************** #
#                            Users Relations Functions                         #
# **************************************************************************** #
from .views_connection import checkToken
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from db_test.models import User, Link


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


@csrf_exempt
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
            friend = User.objects.all().filter(idUser=link.idTarget)[0]
            listeRequest.append({"name": friend.username, "pp" : "/static/" + friend.profilPicture.name, "status" : friend.status, "id" : friend.idUser})
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
            friend = User.objects.all().filter(idUser=link.idTarget)[0]
            listeRequest.append({"name": friend.username, "pp" : "/static/" + friend.profilPicture.name, "status" : friend.status })
        except:
            continue
    return JsonResponse({"success": True, "content" : "", "listcontact" : listeRequest })


@csrf_exempt
def get_can_be_invited(request):
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)

    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    linkFriendRequestList = Link.objects.all().filter(idUser=user.idUser, link=2)
    listeRequest = []
    for link in linkFriendRequestList :
        try:
            friend = User.objects.all().filter(idUser=link.idTarget)[0]
            if friend.status == 1:
                listeRequest.append({"name": friend.username,
                                     "pp" : "/static/" + friend.profilPicture.name,
                                     "status" : friend.status, "id" : friend.idUser})
        except:
            continue
    return JsonResponse({"success": True, "content" : "", "listcontact" : listeRequest })
