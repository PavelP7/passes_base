from django.db import models

class Users(models.Model):
    email = models.EmailField(unique=True)
    fam = models.TextField()
    name = models.TextField()
    otc = models.TextField()
    phone = models.TextField(max_length=12)

class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

class Levels(models.Model):
    winter = models.TextField(max_length=2, blank=True)
    summer = models.TextField(max_length=2, blank=True)
    autumn = models.TextField(max_length=2, blank=True)
    spring = models.TextField(max_length=2, blank=True)

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

    add_time = models.TextField(default="")
    beauty_title = models.TextField()
    title = models.TextField()
    other_titles = models.TextField()
    connect = models.TextField(blank=True)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    level = models.OneToOneField(Levels, on_delete=models.CASCADE)
    status = models.CharField(choices=STATES, default=NEW)

def upload_to(instance, filename):
    return 'images/{pereval}/{filename}'.format(pereval=instance.pereval.title, filename=filename)

class Image(models.Model):
    data = models.ImageField(upload_to=upload_to, blank=True)
    title = models.TextField()
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)

class PerevalAreas(models.Model):
    id_parent = models.IntegerField()
    title = models.TextField()

class UserPereval(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
