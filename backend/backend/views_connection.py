# **************************************************************************** #
#                                Check Functions                               #
# **************************************************************************** #
import hashlib, jwt, random, os
import backend.settings as settings
import requests

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from db_test.models import User, connectionPassword, connection42
from django.shortcuts import render
from django.contrib import messages



@csrf_exempt
def checkLogin(request):
    username = request.POST.get('login')
    password = request.POST.get('password')

    username_check = User.objects.all().filter(username=username)
    if len(username_check) == 0:
        return JsonResponse({"success" : False, "error" : "Username does not exist"})

    password_check = connectionPassword.objects.all().filter(idUser=username_check[0].idUser)
    if len(password_check) == 0:
        return JsonResponse({"success" : False, "error" : "No password authentification"})

    hash = hashlib.sha512(password.encode(), usedforsecurity=True)
    if hash.hexdigest() != password_check[0].password:
        return JsonResponse({"success" : False, "error" : "Password incorrect"})
    token = jwt.encode({"userId": username_check[0].idUser}, settings.SECRET_KEY, algorithm="HS256")

    #username_check[0].tokenJWT = token
    #User.save()

    return JsonResponse({"success" : True, "token" : token})


@csrf_exempt
def checkSignin(request):
    username = request.POST.get('login2')
    password = request.POST.get('password2')
    passwordconfirm = request.POST.get('confirm')

    if not username or password == "" or passwordconfirm == "":
        return JsonResponse({"success" : False, "error" : "Empty field aren't accept"})

    test = User.objects.all().filter(username=username)
    if len(test):
        return JsonResponse({"success" : False, "error" : "Username already use"})

    if password != passwordconfirm:
        return JsonResponse({"success" : False, "error" : "Password and confirm aren't the same"})

    hashPwd = hashlib.sha512(password.encode(), usedforsecurity=True)

    id = User.objects.all().count() + 1
    idType = 1

    token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
    try:
        str = ["images/default/Scout.png", "images/default/Driller.png", "images/default/Engineer.png", "images/default/Soldier.png"]
        user = User(idUser=id, idType=idType, username=username, profilPicture=str[random.randint(0,3)], tokenJWT=token, money=id, idStatus=0)
        user.save()
    except:
        return JsonResponse({"success" : False, "error" : "Error on user creation"})

    try:
        password = connectionPassword(idPassword=id, password=hashPwd.hexdigest(), idUser=user)
        password.save()
    except:
        return JsonResponse({"success" : False, "error" : "Error on password creation"})

    return JsonResponse({"success" : True, "token" : token})


@csrf_exempt
def changePassword(request):
    currentPassword = request.POST.get('currentPass')
    newPassword = request.POST.get('newPass')
    newPasswordComfirm = request.POST.get('newPassConfirm')
    check = checkToken(request)
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
        
    password_check = connectionPassword.objects.all().filter(idUser=user.idUser)
    if (len(password_check) != 0): #if user has a password
        password_check = password_check[0]
        hash = hashlib.sha512(currentPassword.encode(), usedforsecurity=True)
        if hash.hexdigest() != password_check.password:
            return JsonResponse({"success" : False, "error" : "Wrong account password, please try again !"})
    else :			#if user hasn't a password
        password_check = connectionPassword(idPassword=user.idUser, password="", idUser=user)
    if newPassword != newPasswordComfirm:
        return JsonResponse({"success" : False, "error" : "New password is different from new password confirmation, please try again !"})
    else:
        hashPwd = hashlib.sha512(newPassword.encode(), usedforsecurity=True)
        try:
            hashPwd = hashlib.sha512(newPassword.encode(), usedforsecurity=True)
            password_check.password = hashPwd.hexdigest()
            password_check.save()
        except:
            return JsonResponse({"success" : False, "error" : "Somethink very wrong appened, please try again !"})
    return JsonResponse({"success" : True})

@csrf_exempt
def changeUsername(request):
    newName = request.POST.get('newName')
    check = checkToken(request)
    userId = check["userId"]
    user = User.objects.all().filter(idUser=userId)[0]
    user1 = User.objects.all()

    i = 0
    while i < len(user1):
        if user1[i].username == newName:
            if user1[i].idUser != userId:
                return JsonResponse({"success" : False, "error" : "This Username is already taken !"})
        i = i + 1
    if newName == user.username:
        return JsonResponse({"success" : False, "error" : "This is already your Username !"})
    else:
        try:
            user.username = newName
            user.save()
        except:
            return JsonResponse({"success" : False, "error" : "Somethink very wrong appened, please try again !"})
        return JsonResponse({"success" : True})


@csrf_exempt
def checkToken(request):
    token = request.COOKIES.get('token', None)

    if token == None or token == "undefined":
        return {"success" : False, "error" : "No token send"}

    data = None
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    except Exception as error:
        return {"success" : False, "error" : "Token undecodable - " + str(error)}

    userId = data["userId"]
    users = User.objects.all().filter(idUser=userId)
    if len(users) == 0:
        return {"success" : False, "error" : "User id invalid"}
    if len(users) > 1:
        return {"success" : False, "error" : "User id duplicate"}

    if users[0].tokenJWT != token:
        return {"success" : False, "error" : "Invalid token"}

    return {"success" : True, "userId" : userId}

def checkApi42Request(request, islogin, user):
    code = request.GET.get('code')
	# First request : get an users tocken
    i = 1
    j = 0
    if not islogin :
        ListUser = User.objects.all()
        while j < len(ListUser):
            if user.money < ListUser[j].money:
                i = i + 1
            j = j + 1
    websiteUrl = os.getenv('WEBSITE_URL')
    params = \
    {
        "grant_type": "authorization_code",
		"client_id": "u-s4t2ud-1b900294f4f0042d646cdbafdf98a5fe9216f3efd76b592e56b7ae3a18a43bd1",
		"client_secret": os.getenv('API_KEY'),
		"code": code,
		"redirect_uri": websiteUrl + "/3" if islogin else websiteUrl + "/9",
		
    }
    response = requests.post("https://api.intra.42.fr/oauth/token", params=params)
    if response.status_code != 200:
        if not islogin :
            return render(request, "profil_content_full.html", {'user': user, 'pos': i, '42urllink' : os.getenv('WEBSITE_URL')})
        else :
            return render(request, "signin_full.html",{'42urllink' : os.getenv('WEBSITE_URL')})
    response = response.json()
    tocken = response["access_token"]
    headers= {'Authorization': 'Bearer {}'.format(tocken)}
    response = requests.get("https://api.intra.42.fr/v2/me", headers=headers)
    if response.status_code != 200:
        if not islogin :
            return render(request, "profil_content_full.html", {'user': user, 'pos': i, '42urllink' : os.getenv('WEBSITE_URL')})
        else :
            return render(request, "signin_full.html",{'42urllink' : os.getenv('WEBSITE_URL')})
    response = response.json()
    test = connection42.objects.all().filter(login=response["id"])
    if (not islogin) :
        if len(test) == 0:
            try :
                password42 = connection42(login=response["id"], idUser=user)
                password42.save()
            except:
                user = user
        return render(request, "profil_content_full.html", {'user': user, 'pos': i, '42urllink' : os.getenv('WEBSITE_URL')})
	#not already log
    if len(test) == 0:
        id = User.objects.all().count() + 1
        idType = 1

        token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
        username = response["login"]
        number = 0
        while User.objects.all().filter(username=username):
            username = response["login"] + str(number)
            number+=1
            if number > 99 :
                response["login"] = ""
        try:
            imgpath = ["images/default/Scout.png", "images/default/Driller.png", "images/default/Engineer.png", "images/default/Soldier.png"]
            user = User(idUser=id, idType=idType, username=username, profilPicture=imgpath[random.randint(0,3)], tokenJWT=token, money=0, idStatus=0)
            user.save()
            password42 = connection42(login=response["id"], idUser=user)
            password42.save()
        except:
            return render(request, "login_full.html",{'42urllink' : os.getenv('WEBSITE_URL')})
        return render(request, "mainpage_full_tocken42.html", {'user': user})
	#not already log
    else:
        try:
            user = User.objects.all().filter(connection42=test[0])[0]
        except:
            return render(request, "login_full.html",{'42urllink' : os.getenv('WEBSITE_URL')})
        return render(request, "mainpage_full_tocken42.html", {'user': user})
