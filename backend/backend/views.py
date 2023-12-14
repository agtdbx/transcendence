# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/12/14 11:53:38 by hde-min          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import hashlib, sys

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from django.shortcuts import render

from db_test.models import User
from db_test.models import Status
from db_test.models import connectionPassword


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
        user = User.objects.all()
        return render(request,"navbar.html", {'user': user[0] })
    elif num == 1:                      #login classique
            username = request.POST.get('login')
            password = request.POST.get('password')


            username_check = User.objects.all().filter(username=username)
            if len(username_check) == 0:
                return HttpResponse("Username not here")
            
            password_check = connectionPassword.objects.all().filter(idUser=username_check[0].idUser)
            if len(password_check) == 0:
                return HttpResponse("42 user should use superior 42 login method")
            
            hash = hashlib.sha512(password.encode(), usedforsecurity=True)
            if hash.hexdigest() != password_check[0].password:
                return HttpResponse("Wrong password")

            #return HttpResponse(user[0].username)
            return render(request,"mainpage.html")
    elif num == 2:       #aller  a la main page en sign in
        if request.method == 'POST':
            username = request.POST.get('login2')
            password = request.POST.get('password2')
            passwordconfirm = request.POST.get('confirm')
            
            test = User.objects.all().filter(username=username)
            if len(test):
                return HttpResponse("Username already use")
            
            if password != passwordconfirm:
                return render(request,"index.html")

            hashPwd = hashlib.sha512(password.encode(), usedforsecurity=True)
            
            id = User.objects.all().count() + 1
            idType = 1
            
            status= Status(idStatus='0', name="On")
            status.save()

            if not username or password == "":
                return HttpResponse("No empty fields") 
            
            user = User(idUser=id, idType=idType, username=username, profilPicture="NULL", tokenJWT="NULL", money=0, idStatus=Status.objects.get(idStatus=0))
            user.save()
            
            password = connectionPassword(idPassword=id, password=hashPwd.hexdigest(), idUser=user)
            password.save()
            return render(request,"mainpage.html")
        else:
            return HttpResponse("Cheh mechant pti hacker")
    elif num == 3:
        return render(request,"mainpage.html")#aller  a la main page deja connecters
    elif num == 4:
        return render(request,"waitpage.html")
    elif num == 5:
        return render(request,"createGameRoom.html")
    elif num == 6:
        return render(request,"tournament.html")
    elif num == 7:
        return render(request,"profil_content.html")
    elif num == 8:
        return render(request,"index.html")
    else:
        raise Http404('No such section')
