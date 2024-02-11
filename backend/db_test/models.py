from django.db import models
from .validators import validate_file_size

# stock :
#	on_delete=models.CASCADE
#
#

class User(models.Model):
    idUser          = models.IntegerField(primary_key=True)                                                     #[primary key]
    type            = models.IntegerField()
    username        = models.CharField(max_length=15, unique=True)                                              #[unique]
    profilPicture   = models.ImageField(upload_to='images/', verbose_name="", validators=[validate_file_size])
    tokenJWT        = models.TextField()
    money           = models.IntegerField()
    status          = models.IntegerField()


class connectionPassword(models.Model):
    idPassword      = models.IntegerField(primary_key=True)                                                     #[primary key]
    password        = models.TextField()
    idUser          = models.OneToOneField(User, on_delete=models.PROTECT)


class connection42(models.Model):
    login           = models.CharField(max_length=10, primary_key=True)                                         #[primary key]
    idUser          = models.OneToOneField(User, on_delete=models.PROTECT)


class Achivement(models.Model):
    idUser          = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)                    #[primary key]
    winner          = models.IntegerField(default=0)
    perfectShoot    = models.IntegerField(default=0)
    boscoFriend     = models.IntegerField(default=0)
    digGrave        = models.IntegerField(default=0)
    fallen          = models.IntegerField(default=0)
    unpredictable   = models.IntegerField(default=0)
    faster          = models.IntegerField(default=0)
    waveComming     = models.IntegerField(default=0)
    notPassed       = models.IntegerField(default=0)
    friend          = models.IntegerField(default=0)
    party           = models.IntegerField(default=0)
    molyBattle      = models.IntegerField(default=0)


class Link(models.Model):
    id              = models.IntegerField(primary_key=True)                                                     # TRUE [primary key]
    idUser          = models.ForeignKey(User, on_delete=models.PROTECT)                                         #[primary key]
    idTarget        = models.IntegerField()                                                                     #[primary key]
    link            = models.IntegerField()


class PrivMessage(models.Model):
    id              = models.IntegerField(primary_key=True)                                                     # TRUE [primary key]
    idUser          = models.ForeignKey(User, on_delete=models.PROTECT)                                         #[primary key]
    date            = models.TimeField()                                                                        #[primary key]
    data            = models.TextField()
    idTarget        = models.IntegerField()


class Message(models.Model):
    id              = models.IntegerField(primary_key=True)                                                     # TRUE [primary key]
    idUser          = models.ForeignKey(User, on_delete=models.PROTECT)                                         #[primary key]
    date            = models.TimeField()                                                                        #[primary key]
    data            = models.TextField()


class Map(models.Model):
    idMap           = models.IntegerField(primary_key=True)                                                     #[primary key]
    name            = models.CharField(max_length=50)


class Match(models.Model):
    idMatch         = models.IntegerField(primary_key=True)                                                     #[primary key]
    matchDate       = models.TimeField()
    matchDuration   = models.TimeField()
    idMap           = models.ForeignKey(Map, on_delete=models.PROTECT)
    powerUp         = models.BooleanField()
    cursed          = models.BooleanField()
    tournament      = models.BooleanField()


class MatchUser(models.Model):
    id              = models.IntegerField(primary_key=True)                                                     # TRUE [primary key]
    idMatch         = models.ForeignKey(Match, on_delete=models.PROTECT)                                        #[primary key]
    idUser          = models.ForeignKey(User, on_delete=models.PROTECT)                                         #[primary key]
    score           = models.IntegerField()
    powerUp         = models.IntegerField()


class Goal(models.Model):
    id              = models.IntegerField(primary_key=True)                                                     # TRUE [primary key]
    idUser          = models.ForeignKey(User, on_delete=models.PROTECT)                                         #[primary key]
    goalTimer       = models.TimeField()                                                                        #[primary key]
    idMatch         = models.ForeignKey(Match, on_delete=models.PROTECT)                                        #[primary key]
    nbBounce        = models.IntegerField()
    perfectedShot   = models.BooleanField()
    ballSpeed       = models.IntegerField()
    ownGoal         = models.BooleanField()
