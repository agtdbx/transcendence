# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/11/30 14:39:27 by hde-min          ###   ########.fr        #
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

def profil(request):
    return render(request,"profil_content.html")

# def testJS(request):
#     return render(request,"other.html")
	
@csrf_exempt
def testPY(request):
    return HttpResponse("success")


def index2(request):
    return render(request, 'index.html')

randomstring = ["This is section 1.","This is section 2.", "This is section 3."]

def section(request, num):
    if num == 0:
        return render(request,"navbar.html")
    elif num == 1:
        return render(request,"mainpage.html")
    elif num == 2:
        return render(request,"waitpage.html")
    elif num == 3:
        return render(request,"createGameRoom.html")
    elif num == 4:
        return render(request,"tournament.html")
    elif num == 4:
        return render(request,"other.html")
    else:
        raise Http404('No such section')
