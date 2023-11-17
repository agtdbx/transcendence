# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/08 14:00:09 by lflandri          #+#    #+#              #
#    Updated: 2023/11/17 16:38:53 by hde-min          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
  return render(request,"index.html")
