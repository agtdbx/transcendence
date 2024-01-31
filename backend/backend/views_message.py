# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_message.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/23 19:48:56 by aderouba          #+#    #+#              #
#    Updated: 2024/01/31 13:49:41 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# **************************************************************************** #
#                            DB connexion Functions                            #
# **************************************************************************** #
from .views_connection import checkToken
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from db_test.models import User, Message, PrivMessage, Link


def key_sort_per_date(obj):
    return obj.date


@csrf_exempt
def getMessages(request):
    if request.method != 'POST':
        return JsonResponse({"success" : False, "error" : "Need to pass by post"})

    # Check token
    check = checkToken(request)
    if check["success"] == False:
        return JsonResponse({"success" : False, "error" : "Token invalid"})

    test = User.objects.all().filter(idUser=check["userId"])
    if len(test) != 1:
        return JsonResponse({"success" : False, "error" : "Missing user"})

    myUser = test[0]

    lastMessagesLoad = 0
    channel = ""

    try:
        lastMessagesLoad = request.POST.get("lastMessagesLoad")
        if lastMessagesLoad == "null" or lastMessagesLoad == None:
            return JsonResponse({"success" : False, "error" : "Bad lastMessagesLoad : " + str(lastMessagesLoad)})

        lastMessagesLoad = int(lastMessagesLoad)

        channel = request.POST.get("channel")

        if channel != "general":
            channel = int(channel)

    except Exception as error:
        return JsonResponse({"success" : False, "error" : "Get lastMessagesLoad or channel don't work : " + str(error)})

    linkFriendRequestList = Link.objects.all().filter(idUser=myUser.idUser, link=3)
    blockedUsers = []
    for link in linkFriendRequestList :
        try:
            friend = User.objects.all().filter(idUser=link.idTarget)[0]
            blockedUsers.append(friend.idUser)
        except:
            continue

    if channel == "general":
        msgs = Message.objects.all().order_by("date")

        for id in blockedUsers:
            msgs = msgs.exclude(idUser=id)

        if lastMessagesLoad == -1:
            lastMessagesLoad = len(msgs)

        start = max(0, lastMessagesLoad - 10)
        end = lastMessagesLoad

        messages = []
        for i in range(start, end):
            msg = msgs[i]
            idUser = int(msg.idUser.idUser)
            users = User.objects.all().filter(idUser=idUser)
            user = users[0]
            message = [msg.id, user.username, "/static/" + str(user.profilPicture), msg.date, msg.data]
            messages.append(message)
        return JsonResponse({"success" : True, "messages" : messages, "lastMessagesLoad" : start})

    else:
        msgs = list(PrivMessage.objects.all().filter(idUser=myUser.idUser).filter(idTarget=channel))
        msgs.extend(list(PrivMessage.objects.all().filter(idUser=channel).filter(idTarget=myUser.idUser)))

        msgs.sort(key=key_sort_per_date)

        if lastMessagesLoad == -1:
            lastMessagesLoad = len(msgs)

        start = max(0, lastMessagesLoad - 10)
        end = lastMessagesLoad

        messages = []
        for i in range(start, end):
            msg = msgs[i]
            idUser = int(msg.idUser.idUser)
            users = User.objects.all().filter(idUser=idUser)
            user = users[0]
            message = [msg.id, user.username, "/static/" + str(user.profilPicture), msg.date, msg.data]
            messages.append(message)
        return JsonResponse({"success" : True, "messages" : messages, "lastMessagesLoad" : start})
