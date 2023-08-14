from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
user_choice = (
    ('manager','Manager'),
    ('user','user')    # first used in database link and second Display name    
)

gender_choice = (
    ('male','Male'),
    ('female','Famale')
)

user_mode = (
    ('kid','kid'),
    ('teenager','teenager'),
    ('adult','adult'),
    ('alder','alder')
)

class CustomUser(AbstractUser):
    mode = models.CharField(max_length=10,choices=user_mode,default='kid')
    user_type = models.CharField(max_length=10,choices=user_choice,default='user')
    address = models.CharField(max_length=600,blank=True,null=True)
    contact = models.CharField(max_length=10,default='')
    gender = models.CharField(max_length=50,choices=gender_choice,default='male')
    age = models.IntegerField(default=0)
    b_date = models.DateField(default=timezone.now)
    about = models.CharField(max_length=700,blank=True,null=True)
    p_img = models.ImageField(upload_to='photos/', blank=True,null=True)