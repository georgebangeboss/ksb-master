from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ksb import settings

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        employee_number,
        password=None,
        is_active=True,
        is_staff=False,
        is_admin=False,
    ):
        if not email:
            raise ValueError("User must have an email address")
        if not employee_number:
            raise ValueError("User must have an employee number")
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(
            email=self.normalize_email(email),
            employee_number=employee_number,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self.db)
        return user_obj

    def create_staffuser(
        self,
        email,
        employee_number,
        password=None,
    ):
        staff_user_obj = self.create_user(
            email, employee_number, password=password, is_staff=True
        )

        return staff_user_obj

    def create_superuser(
        self,
        email,
        employee_number,
        password=None,
    ):
        staff_user_obj = self.create_user(
            email, employee_number, password=password, is_staff=True, is_admin=True
        )

        return staff_user_obj


# sub-classing AbstractBaseUser gives us id,password and last-login fields all we gotta do is add the rest
class User(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)  # can log in
    staff = models.BooleanField(default=False)  # engineers,managers and salespersons
    admin = models.BooleanField(default=False)  # isSuperUser

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    employee_number = models.CharField(max_length=255)
    confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    # By default USERNAME_FIELD and password are required fields ,to add your own use REQUIRED_FIELDS
    REQUIRED_FIELDS = [
        "employee_number",
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return f"{self.first_name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Engineer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class SalesPerson(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
