# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/11/17 18:24:08 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
 

def index(request):
  return render(request,"index.html")

def testJS(request):
    return render(request,"other.html")
	
@csrf_exempt
def testPY(request):
    return HttpResponse("success")
