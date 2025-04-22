
from django.conf import settings
import random
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin,AbstractBaseUser
from twilio.rest import Client  
from dotenv import load_dotenv 
import os
load_dotenv() 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not phone_number:
            raise ValueError("Phone number is required")

        email = self.normalize_email(email)
        extra_fields.pop("username", None)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        #admin babu@gmail.com
        user.save(using=self._db)
        print(email)
        return user

    def create_superuser(self, email,phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user( email,phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Only active after OTP verification
  # ✅ Add missing fields required by Django
    is_staff = models.BooleanField(default=False)  # Required for Django admin access
    is_superuser = models.BooleanField(default=False)  # Required for Django admin permissions
    objects = CustomUserManager()
       # Set the email field as the login field
    USERNAME_FIELD = "email"  # Change to email
    REQUIRED_FIELDS = ["phone_number"]  # Ensure phone_number is required
    # USERNAME_FIELD = "phone_number"
    # REQUIRED_FIELDS = ["email"]  # Ensure email is required

    
    def generate_otp(self):
       
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp

    def verify_otp(self, otp):
        # Check if OTP matches and is valid within 5 minutes
        if self.otp == otp and (timezone.now() - self.otp_created_at).seconds < 300:
            self.is_active = True
            self.otp = None  # Clear OTP after verification
            self.save()
            return True
        return False

    def send_otp_sms(self):
        try:
            otp = self.generate_otp()
          
            account_sid = os.getenv("ACCOUNT_SID")
            auth_token = os.getenv("AUTH_TOKEN")
            client = Client(account_sid, auth_token)
            
            message = client.messages.create(
                body=f"Your OTP is {otp}",
                from_=os.getenv("PHONENUMBER"),
              
                to=self.phone_number
            )
            
            
            def __str__(self):
                return self.phone_number

    

        except Exception as e:
            print("Twilio OTP Send Error:", str(e))  # Add this!
            return None

class Profile(models.Model):
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # Personal Information
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    
    # Birth Information
    borndistrict = models.CharField(max_length=100)
    bornward = models.IntegerField(blank=True, null=True)
    bornplace = models.CharField(max_length=100)

    # Current Address
    currentdistrict = models.CharField(max_length=100)
    currentward = models.IntegerField(blank=True, null=True)
    currentplace = models.CharField(max_length=100)

    # Citizenship Details
    citizennumber = models.CharField(max_length=50, unique=True)
    issuedate = models.DateField()
    issueplace = models.CharField(max_length=100)

    # Images
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    frontimage = models.ImageField(upload_to="citizenship_front/", blank=True, null=True)
    backimage = models.ImageField(upload_to="citizenship_back/", blank=True, null=True)

    # Family Information
    father_firstname = models.CharField(max_length=50)
    father_middlename = models.CharField(max_length=50, blank=True, null=True)
    father_lastname = models.CharField(max_length=50)
    father_borndistrict = models.CharField(max_length=100)
    father_bornward = models.IntegerField(blank=True, null=True)
    father_bornplace = models.CharField(max_length=100)

    mother_firstname = models.CharField(max_length=50)
    mother_middlename = models.CharField(max_length=50, blank=True, null=True)
    mother_lastname = models.CharField(max_length=50)
    mother_borndistrict = models.CharField(max_length=100)
    mother_bornward = models.IntegerField(blank=True, null=True)
    mother_bornplace = models.CharField(max_length=100)

    partner_firstname = models.CharField(max_length=50, blank=True, null=True)
    partner_middlename = models.CharField(max_length=50, blank=True, null=True)
    partner_lastname = models.CharField(max_length=50, blank=True, null=True)
    partner_borndistrict = models.CharField(max_length=100, blank=True, null=True)
    partner_bornward = models.IntegerField(blank=True, null=True)
    partner_bornplace = models.CharField(max_length=100, blank=True, null=True)
    def clean(self):
        if self.gender not in dict(self.GENDER_CHOICES):
            raise ValidationError("Invalid gender selected")
    def __str__(self):
        return f"{self.firstname} {self.lastname}"