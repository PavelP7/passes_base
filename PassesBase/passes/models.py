from django.db import models

class Users(models.Model):
    email = models.EmailField(unique=True)
    fam = models.TextField()
    name = models.TextField()
    otc = models.TextField()
    phone = models.TextField(max_length=12)

class Coords(models.Model):
    latitude = models.FloatField()
    longtitude = models.FloatField()
    height = models.IntegerField()

class PerevalAdded(models.Model):
    NEW = 'NW'
    PENDING = 'PD'
    ACCEPTED = 'AC'
    REJECTED = 'RJ'

    STATES = [
        (NEW, 'new'),
        (PENDING, 'pending'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected')
    ]

    date_added = models.DateTimeField()
    beautyTitle = models.TextField()
    title = models.TextField()
    other_titles = models.TextField()
    connect = models.TextField(blank=True)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    level_winter = models.TextField(max_length=2, blank=True)
    level_summer = models.TextField(max_length=2, blank=True)
    level_autumn = models.TextField(max_length=2, blank=True)
    level_spring = models.TextField(max_length=2, blank=True)
    status = models.CharField(choices=STATES, default=NEW)

class Image(models.Model):
    data = models.ImageField(upload_to='images/')
    title = models.TextField()
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)

class PerevalAreas(models.Model):
    id_parent = models.IntegerField()
    title = models.TextField()
