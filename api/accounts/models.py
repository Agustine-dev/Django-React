from collections.abc import Iterator
import os
from PIL import Image

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin,Group
from django.core.validators import RegexValidator
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.shortcuts import resolve_url
from rest_framework.authtoken.models import Token


# Create your models here.
# User Manager
class UserManager(BaseUserManager):
    # create user
    def create_user(self,username,email,telephone,password=None):
        if not email:
            raise ValueError('Enter a valid email')
        if not username:
            raise ValueError("Enter a valid User's Name")
        if not telephone:
            raise ValueError("Enter a valid Telephone or Mobile number")
    
        
        user = self.model(username=username,email=self.normalize_email(email),telephone=telephone,password=password)
        user.set_password(password)
        Token.objects.create(user=user)
        user.save(using=self._db)
        return user
     # create staff user
    def create_staffuser(self,username, email,telephone, password):
       user = self.create_user(username,email,telephone, password)
       user.staff = True
       Token.objects.create(user=user)
       user.save(using=self._db)
       return user
    
    # create super user / admin
    def create_superuser(self,username,email,telephone, password):
        user = self.create_user(username=username,email=email,telephone=telephone,password=password)
        user.staff = True
        user.admin = True
        Token.objects.create(user=user)
        user.save(using=self._db)
        return user



# User Types
class Types(models.TextChoices):
    COURIER = "COURIER", 'courier'
    RESTRAUNT = "RESTRAUNT","restraunt"
    CLIENT = "CLIENT", "client"

# user model
class User(AbstractBaseUser):    
    username = models.CharField(max_length=15,unique=True)
    email = models.EmailField(max_length=245, unique=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    user_type = models.CharField(max_length=10, choices=Types.choices, default=Types.CLIENT)
    is_courier = models.BooleanField(default=False)
    is_restraunt = models.BooleanField(default=False)
    telephone = models.CharField(
        max_length=16,
        verbose_name=_('Telephone'),
        blank=True,
        validators=(RegexValidator(
            getattr(settings, 'TELEPHONE_REGEXP', r'^(\+[254]\d{10,11})?$')
        ),)
    )

     # username replaced with email
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'telephone']


    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self,perm, obj=None):
        return self.admin
    
    def has_module_perms(self, app_label):
        return True
    
    
    @property
    def is_staff(self):
        if self.staff:
            return True
        else:
            return False
        
    def save(self, *args, **kwargs):
        if not self.user_type:
            self.user_type = User.Types.CLIENT
        return super().save(*args,**kwargs)

# img rename
def img_uploader(instance,filename):
  # fpath = pathlib.Path(filename)
  # new_fname = str(instance.user)
  # file
  return os.path.join('profiles_img', instance.user.email,filename)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=245)
    last_name = models.CharField(max_length=245)
    GENDER_TYPES = (
        ('ml',_("Male")),
        ('fl',"Female")
    )
    gender = models.CharField(_('Gender'), max_length=2, default=GENDER_TYPES[0][0],choices=GENDER_TYPES)
    img = models.ImageField(upload_to=img_uploader, null=True, blank=True)
    bio = models.CharField(max_length=245, null=True, blank=True)
    address = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class CourierManager(models.Manager):
    # create user
    def create_user(self,username,email,telephone,password=None):
        if not email:
            raise ValueError('Enter a valid email')
        if not username:
            raise ValueError("Enter a valid User's Name")
        if not telephone:
            raise ValueError("Enter a valid Telephone or Mobile number")
    
        
        user = self.model(username=username,email=self.normalize_email(email),telephone=telephone,password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def get_queryset(self,*args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user_type=User.Types.COURIER)
        return qs

class Courier(User):

    class Meta:
        proxy = True
    
    objects = CourierManager()

    
    def save(self,*args, **kwargs):
        self.user_type = User.Types.COURIER
        self.is_courier = True
        return super().save(*args, **kwargs)
    
    