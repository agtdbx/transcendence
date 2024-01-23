# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    api.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/23 19:48:38 by aderouba          #+#    #+#              #
#    Updated: 2024/01/23 20:00:20 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def gameAPI(request):
    # For create data
    if request.method == 'POST':
        pass
    # For get data
    if request.method == 'GET':
        pass
    # For update data
    if request.method == 'PUT':
        pass
    # For delete data
    if request.method == 'DELETE':
        pass

    return JsonResponse({"success" : False, "error" : "Invalid method"})
