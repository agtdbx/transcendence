# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/11/22 15:49:38 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import sys
 

def index(request):
    # print >>sys.stderr, 'Goodbye, cruel world!'
    print(request, file=sys.stderr)
    if request.method == "POST" and request.POST["page"] == "profil":
        print(request, file=sys.stderr)
        return render(request,"profil_content.html")
    else :
    	return render(request,"index.html")

def testJS(request):
    return render(request,"other.html")
	
@csrf_exempt
def testPY(request):
    return HttpResponse("success")
