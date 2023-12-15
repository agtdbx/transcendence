# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/12/15 17:53:38 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from django.shortcuts import render

from db_test.models import User
from db_test.models import Status


# def testJS(request):
#     return render(request,"other.html")
	
@csrf_exempt
def testPY(request):
    return HttpResponse("success")


def index(request):
    return render(request, 'index.html')

randomstring = ["This is section 1.","This is section 2.", "This is section 3."]

def section(request, num):
    if num == 0:
        return render(request,"navbar.html")
    elif num == 1:
        if request.method == 'POST':
            username = request.POST.get('login')
            idUser = request.POST.get('password')
            idType = idUser

            # Create a new patient entry in the database using the Patient model

            status= Status(idStatus='0', name="Online")
            status.save()

            user = User(idUser=idUser, idType=idType, username=username, profilPicture="wrgsd", tokenJWT="wgdsv", money=1, idStatus=Status(idStatus='0', name="Online"))
            user.save()
            return render(request,"mainpage.html")
        else:
            return HttpResponse("Invalid request method.")
    elif num == 2:
        return render(request,"waitpage.html")
    elif num == 3:
        return render(request,"createGameRoom.html")
    elif num == 4:
        return render(request,"tournament.html")
    elif num == 5:
        return render(request,"profil_content.html")
    elif num == 6:
        return render(request,"index.html")
    else:
        raise Http404('No such section')

def user(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        idUser = request.POST.get('password')
        idType = idUser

        # Create a new patient entry in the database using the Patient model

        status= Status(idStatus='0', name="Online")
        status.save()

        user = User(idUser=idUser, idType=idType, username=username, profilPicture="wrgsd", tokenJWT="wgdsv", money=1, idStatus=Status(idStatus='0', name="Online"))
        user.save()



        return render(request,"mainpage.html")
    else:
        return HttpResponse("Invalid request method.")

def gamePage(request):
	return render(request,"game.html")
