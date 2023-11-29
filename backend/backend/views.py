# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/11/29 16:04:26 by hde-min          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from django.shortcuts import render

# def index(request):
#     return render(request,"index.html")

def mainPage(request):
  return render(request,"mainpage.html")

def waitPage(request):
  return render(request,"waitpage.html")

def ladderPage(request):
  return render(request,"ladder.html")

def createtournaPage(request):
  return render(request,"tournamentcreate.html")

def tournaPage(request):
  return render(request,"tournament.html")

def cgp(request):
  return render(request,"createGameRoom.html")
 

def index(request):
  return render(request,"index.html")

def testJS(request):
    return render(request,"other.html")
	
@csrf_exempt
def testPY(request):
    return HttpResponse("success")
