import os, hashlib
from db_test.models import User, connectionPassword, Map

test = User.objects.all().filter(username="Karl")
# If Karl doesn't exist, create Karl
if len(test) == 0:
    username = "karl"
    password = os.getenv('ADMIN_PWD')
    hashPwd = hashlib.sha512(password.encode(), usedforsecurity=True)
    id = 1
    idType = 2
    user = User(idUser=id, type=idType, username=username,
             profilPicture="images/default/Karl.png",
             money=100000, status=0)
    user.save()
    password = connectionPassword(idPassword=id, password=hashPwd.hexdigest(),
                               idUser=user)
    password.save()


test = User.objects.all().filter(username="Bosco")
# If Bosco doesn't exist, create it
if len(test) == 0:
    username = "bosco"
    id = -1
    idType = 2
    user = User(idUser=id, type=idType, username=username,
             profilPicture="images/default/Bosco.png",
             money=0, status=0)
    user.save()


test = User.objects.all().filter(username="Mission Control")
# If MissionControl doesn't exist, create it
if len(test) == 0:
    username = "mission control"
    id = 0
    idType = 2
    user = User(idUser=id, type=idType, username=username,
             profilPicture="images/default/MissionControl.png",
             money=0, status=0)
    user.save()


# Create maps
test = Map.objects.all().count()
if test == 0:
    map = Map.objects.create(idMap=0, name="Default Map")
    map.save()
    map = Map.objects.create(idMap=1, name="Sun quest")
    map.save()
    map = Map.objects.create(idMap=2, name="Flipper")
    map.save()
    map = Map.objects.create(idMap=3, name="Pickaxe dance")
    map.save()
    map = Map.objects.create(idMap=4, name="Difficulty 5, verminagedon, no shield")
    map.save()
