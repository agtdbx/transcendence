# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/11/29 13:38:04 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

i = 0

def index(request):
  if i == 0:
    return render(request,"index.html")

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

def profil(request):
    return render(request,"profil_content.html")

# def testJS(request):
#     return render(request,"other.html")
	
# @csrf_exempt
# def testPY(request):
#     return HttpResponse("success")
