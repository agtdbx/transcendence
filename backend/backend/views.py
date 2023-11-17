# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/11/08 14:01:26 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from django.http import HttpResponse
 
def index(request):
    return HttpResponse("Hello, world. You're at the root of the server.");