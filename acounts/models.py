from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, dob,name, tc,password=None,password2=None):
        """
        Creates and saves a User with the given email, date of
        birth , password, name and tc.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            dob=dob,
            tc =tc,
            name=name,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,dob,tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password, name and tc.
        """
        user = self.create_user(
            email,
            password=password,
            dob=dob,
            tc=tc,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address", max_length=255,  unique=True, )
    dob = models.DateField(verbose_name="date of birth",null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    name = models.CharField(verbose_name= "full name", max_length=250)
    user_profile = models.ImageField(verbose_name="profile image", upload_to="profile_images", height_field=64, width_field=64, max_length=255, null=True,blank=True)

    phone_number = models.CharField(
        verbose_name="phone number",
        max_length=10,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be exactly 10 digits.')],
        unique=True,
    )
    tc = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","dob","tc"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
   
    class Meta:
        db_table = 'tbl_user_mstr'
        # app_label = 'user'
        managed = True