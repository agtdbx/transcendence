# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/11/17 17:43:02 by lflandri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from django.http import HttpResponse
from django.shortcuts import render
 

def index(request):
  return render(request,"index.html")

def testJS(request):
    page = "<!DOCTYPE html>"
    page += "<html>"
    page += "<head>"
    page += "    <title>test</title>"
    page += "    <meta charset=\"utf-8\">"
    page += "</head>"
    page += "<body>"
    page += "    <p id=\"lol\">Hello there</p"
    page += "    <div id=\"win_rate\" style=\"background-color: red; padding: 0%; height: 20px; border-radius: 30px\">"
    page += "        <div id=\"progg_bar_win_rate\" style=\"background-color: green; display: inline-block; margin:  0%; width: 0%; height: 20px; border-radius: 30px;\">"
    page += "        </div>"
    page += "    </div>"
    page += "</body>"
    page += "<script type=\"text/javascript\">"
    page += "    function win_rate_calcul(win_rate) {"
    page += "        document.getElementById(\"progg_bar_win_rate\").style.width = \"\" +  (win_rate * 100) +  \"%\"; "
    page += "    }"
    page += "    win_rate_calcul(0.30);"
    page += "    var requete = new XMLHttpRequest();"
    page += "            requete.open(\"POST\", \"http://localhost:4200/pytest\");"
    page += "            requete.setRequestHeader(\"Content-type\", \"application/x-www-form-urlencoded\");"
    page += "			 requete.withCredentials = true;"
    page += "            requete.send(\"test45\" /*content to send*/);"
    page += "            requete.onload = function() {"
    # page += "            //La variable à passer est alors contenue dans l'objet response et l'attribut responseText."
    page += "            var variableARecuperee = this.responseText;"
    page += "            document.getElementById(\"lol\").textContent = variableARecuperee"
    page += "            };"
    page += "</script>"
    return HttpResponse(page)


def testPY(request):
    return ("success")
