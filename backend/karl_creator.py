import os, hashlib, jwt
from db_test.models import User, connectionPassword
import backend.settings as settings

username = "Karl"
password = os.getenv('POSTGRES_PASSWORD')
hashPwd = hashlib.sha512(password.encode(), usedforsecurity=True)
id = 1
idType = 2
token = jwt.encode({"userId": id}, settings.SECRET_KEY, algorithm="HS256")
user = User(idUser=id, idType=idType, username=username, profilPicture="images/default/Karl.png", tokenJWT=token, money=100000, idStatus=0)
user.save()
password = connectionPassword(idPassword=id, password=hashPwd.hexdigest(), idUser=user)
password.save()