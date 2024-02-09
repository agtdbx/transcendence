import  os

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from db_test.models import Tournament
import datetime

from .forms import UserForm
from .views_connection import checkToken
from .views_connection import checkApi42Request


@csrf_exempt
def createTournament(request):
    test = Tournament.objects.all()
    for i in test:
        if (test[i].isStarted == True):
            return ;
    id = len(test)
    tournament = Tournament(idTournament=id, idMap=2, powerUp=False, cursed=False, isStarted=False, isFinished=False)
    tournament.save()