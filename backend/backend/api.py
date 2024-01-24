# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    api.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/23 19:48:38 by aderouba          #+#    #+#              #
#    Updated: 2024/01/24 16:37:34 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def getHelp():
    helpStr =  "HELP :\n"
    helpStr += "Body of request\n"
    helpStr += "    cmd : the command needed(string)\n"
    helpStr += "    ...\n"
    helpStr += "\n"
    helpStr += "\n"
    helpStr += "RETURN CORRECT\n"
    helpStr += "    json{'success':true, 'content'}\n"
    helpStr += "\n"
    helpStr += "\n"
    helpStr += "RETURN ERROR\n"
    helpStr += "    json{'success':false, 'error', 'help'}\n"
    helpStr += "\n"
    helpStr += "\n"
    helpStr += "POST\n"
    helpStr += "    Create Game Room :\n"
    helpStr += "        cmd : 'createRoom'\n"
    helpStr += "        -> 'content' {'roomId'}\n"
    helpStr += "\n"
    helpStr += "\n"
    helpStr += "GET\n"
    helpStr += "    Connection to a game Room\n"
    helpStr += "        cmd : 'connectRoom'\n"
    helpStr += "        roomId : roomId\n"
    helpStr += "        -> 'content' {'paddleId', 'teamId'}\n"
    helpStr += "\n"
    helpStr += "    Get the state of the room\n"
    helpStr += "        cmd : 'stateRoom'\n"
    helpStr += "        roomId : roomId\n"
    helpStr += "        -> 'content' {'powerUpEnable', 'mapChoose', 'paddleList'}\n"
    helpStr += "           'paddleList' : {'teamLeft', 'teamRight'}\n"
    helpStr += "           'team____' : [paddleType, paddleType]\n"
    helpStr += "           'paddleType' : 'null' / 'player' / 'ia'\n"
    helpStr += "\n"
    helpStr += "    \n"
    helpStr += "\n"
    helpStr += "PUT\n"
    helpStr += "\n"
    helpStr += "\n"
    helpStr += "DELETE\n"
    return helpStr


@csrf_exempt
def gameAPI(request):
    # For create data
    if request.method == 'POST':
        pass
    # For get data
    if request.method == 'GET':
        return JsonResponse(getMethodAPI(request))
    # For update data
    if request.method == 'PUT':
        pass
    # For delete data
    if request.method == 'DELETE':
        pass

    return JsonResponse({"success" : False,
                         "error" : "Invalid method",
                         "help" : getHelp()})


def getMethodAPI(request):
    cmd = ""
    try:
        cmd = request.GET.get("cmd")
    except:
        return {"success" : False,
                "error" :"cmd not found",
                "help" : getHelp()}
