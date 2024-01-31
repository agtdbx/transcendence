# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_42link.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/23 20:20:38 by lflandri          #+#    #+#              #
#    Updated: 2024/01/31 13:46:59 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from django.http import JsonResponse
from db_test.models import User, connectionPassword, connection42
from . import views


def checkislinked(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    test = connection42.objects.all().filter(idUser=userId)
    if len(test) == 0:
        return JsonResponse({"success" : False, "error" : "User is not linked."})
    return JsonResponse({"success" : True, "error" : "User is linked."})


def removelink(request):
    check = views.checkToken(request)
    if check["success"] == False:
        return JsonResponse(check)
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    test = connection42.objects.all().filter(idUser=userId)
    if len(test) == 0:
        return JsonResponse({"success" : False, "error" : "User is not linked."})
    mdptest = connectionPassword.objects.all().filter(idUser=userId)
    if len(mdptest) == 0:
        return JsonResponse({"success" : False, "error" : "You don't have a password set. Please set a password before unlink your 42 account."})
    try :
        test[0].delete()
    except :
        return JsonResponse({"success" : False, "error" : "Error when try to remove link of db"})
    return JsonResponse({"success" : True, "error" : "Link to 42 removed"})
