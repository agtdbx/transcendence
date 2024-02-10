import os, hashlib, jwt
from db_test.models import User, connectionPassword
import backend.settings as settings

test = User.objects.all().filter(username="Karl")
# If Karl doesn't exist, create Karl
if len(test) == 0:
    username = "Karl"
    password = os.getenv('ADMIN_PWD')
    hashPwd = hashlib.sha512(password.encode(), usedforsecurity=True)
    id = 1
    idType = 2
    token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
    user = User(idUser=id, type=idType, username=username,
             profilPicture="images/default/Karl.png", tokenJWT=token,
             money=100000, status=0)
    user.save()
    password = connectionPassword(idPassword=id, password=hashPwd.hexdigest(),
                               idUser=user)
    password.save()


test = User.objects.all().filter(username="Bosco")
# If Bosco doesn't exist, create it
if len(test) == 0:
    username = "Bosco"
    id = -1
    idType = 2
    token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
    user = User(idUser=id, type=idType, username=username,
             profilPicture="images/default/Bosco.png", tokenJWT=token,
             money=0, status=0)
    user.save()


test = User.objects.all().filter(username="Mission Control")
# If MissionControl doesn't exist, create it
if len(test) == 0:
    username = "Mission Control"
    id = -2
    idType = 2
    token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
    user = User(idUser=id, type=idType, username=username,
             profilPicture="images/default/MissionControl.png", tokenJWT=token,
             money=0, status=0)
    user.save()

# Create maps
