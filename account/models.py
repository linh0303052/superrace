from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date

class AccountManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, first_name=None, last_name=None, dob=None, gender=None, height=0, weight=0):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            dob = dob,
            gender = gender,
            weight = weight,
            height = height,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, email, password, first_name, last_name, dob, gender, height, weight):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")

        user = self.create_user(
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            dob = dob,
            gender = gender,
            email = self.normalize_email(email),
            height = height,
            weight = weight,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.set_password(password)
        user.save(using = self._db)
        return user

# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(null=False, max_length=60, unique=True)
    username = models.CharField(null=False, unique=True, max_length=30)
    password = models.CharField(null=False, max_length=128)
    first_name = models.CharField(null=False, max_length=128)
    last_name = models.CharField(null=False, max_length=128)
    dob = models.DateField(null=False)
    gender = models.BooleanField(null=False) #True: male, False: female
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name','last_name', 'dob', 'weight', 'height', 'gender']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True