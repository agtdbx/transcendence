# **************************************************************************** #
#                                Check Functions                               #
# **************************************************************************** #
import hashlib, jwt, random
import backend.settings as settings

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from db_test.models import User, connectionPassword


@csrf_exempt
def checkLogin(request):
    username = request.POST.get('login')
    password = request.POST.get('password')

    username_check = User.objects.all().filter(username=username)
    if len(username_check) == 0:
        return JsonResponse({"success" : False, "error" : "Username not exist"})

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
        user = User(idUser=id, idType=idType, username=username, profilPicture=str[random.randint(0,3)], tokenJWT=token, money=0, idStatus=0)
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

    password_check = connectionPassword.objects.all().filter(idUser=user.idUser)[0]
    hash = hashlib.sha512(currentPassword.encode(), usedforsecurity=True)
    if hash.hexdigest() != password_check.password:
        return JsonResponse({"success" : False, "error" : "Wrong account password, please try again !"})
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
