from django.db import models

# stock :
#	on_delete=models.CASCADE
#
#

class Status(models.Model):
    idStatus  = models.IntegerField(primary_key=True)								#[primary key]
    name      = models.CharField(max_length=10)


class User(models.Model):
    idUser        = models.IntegerField(primary_key=True) 			#[primary key]
    idType        = models.IntegerField()
    username      = models.CharField(max_length=10, unique=True)	#[unique]
    profilPicture = models.TextField()
    tokenJWT      = models.TextField()
    money         = models.IntegerField()
    idStatus      = models.ForeignKey(Status, on_delete=models.PROTECT) 


class connectionPassword(models.Model):
    idPassword  = models.IntegerField(primary_key=True) 			#[primary key]
    password    = models.TextField()
    idUser      = models.OneToOneField(User, on_delete=models.PROTECT)


class connection42(models.Model):
    login = models.CharField(max_length=10, primary_key=True)		#[primary key]
    idUser = models.OneToOneField(User, on_delete=models.PROTECT)


class UserType(models.Model):
    idType = models.IntegerField(primary_key=True)									#[primary key]
    name   = models.CharField(max_length=10, unique=True)


class Achivement(models.Model):
    idUser  = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)								#[primary key]
    forKarl = models.BooleanField()


class LinkType(models.Model):
    id    = models.IntegerField(primary_key=True)									#[primary key]
    type  = models.CharField(max_length=50)


class Link(models.Model):
    id    	 = models.IntegerField(primary_key=True)								# TRUE [primary key]
    idUser   = models.ForeignKey(User, on_delete=models.PROTECT)					#[primary key]
    #idTarget = models.ForeignKey(User, on_delete=models.PROTECT)					#[primary key]
    idTarget = models.IntegerField()
    link     = models.ForeignKey(LinkType, on_delete=models.PROTECT) 


class PrivMessage(models.Model):
    id    	 = models.IntegerField(primary_key=True)				# TRUE [primary key]
    idUser    = models.ForeignKey(User, on_delete=models.PROTECT)								#[primary key]
    date      = models.TimeField()									#[primary key]
    data      = models.TextField()
    idTarget  = models.IntegerField()  


class Message(models.Model):
    id    	 = models.IntegerField(primary_key=True)								# TRUE [primary key]
    idUser      = models.ForeignKey(User, on_delete=models.PROTECT)								#[primary key]
    date        = models.TimeField()								#[primary key]
    data        = models.TextField()


class Map(models.Model):
    idMap       = models.IntegerField(primary_key=True)								#[primary key]
    name        = models.CharField(max_length=50)
    background  = models.TextField()
    obstacle    = models.TextField()


class Match(models.Model):
    idMatch        = models.IntegerField(primary_key=True)							#[primary key]
    matchDate      = models.TimeField()
    matchDuration  = models.TimeField()
    idMap          = models.ForeignKey(Map, on_delete=models.PROTECT)  
    powerUp        = models.BooleanField()
    cursed         = models.BooleanField()
    tournament     = models.BooleanField()


class MatchUser(models.Model):
    id    	 = models.IntegerField(primary_key=True)								# TRUE [primary key]
    idMatch = models.ForeignKey(Match, on_delete=models.PROTECT)								#[primary key]
    idUser  = models.ForeignKey(User, on_delete=models.PROTECT)									#[primary key]
    score   = models.IntegerField()  
    powerUp = models.IntegerField()  


class Goal(models.Model):
    id    	 = models.IntegerField(primary_key=True)								# TRUE [primary key]
    idUser        = models.ForeignKey(User, on_delete=models.PROTECT)							#[primary key]
    goalTimer     = models.TimeField()								#[primary key]
    idMatch       = models.ForeignKey(Match, on_delete=models.PROTECT)							#[primary key]
    nbBounce      = models.IntegerField()  
    perfectedShot = models.BooleanField()
    ballSpeed     = models.IntegerField()  
    ownGoal       = models.BooleanField()


class Tournament(models.Model):
    idTournament    = models.IntegerField(primary_key=True)							#[primary key]
    startDate       = models.TimeField()
    nameTournament  = models.CharField(max_length=20)
    nbMaxUser       = models.IntegerField()  
    idMap           = models.ForeignKey(Map, on_delete=models.PROTECT)  
    powerUp         = models.BooleanField()
    cursed          = models.BooleanField()


class UserTournament(models.Model):
    id    	 	  = models.IntegerField(primary_key=True)								# TRUE [primary key]
    idTournament  = models.ForeignKey(Tournament, on_delete=models.PROTECT)							#[primary key]
    idUser        = models.ForeignKey(User, on_delete=models.PROTECT)							#[primary key]
    nickname      = models.CharField(max_length=20, unique=True) 	#[unique]
    rank          = models.IntegerField()  


class MatchTournament(models.Model):
    idMatch      = models.OneToOneField(Match, on_delete=models.PROTECT, primary_key=True)							#[primary key]
    idTournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)

