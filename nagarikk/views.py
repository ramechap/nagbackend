import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET
from .forms import OTPVerificationForm, ProfileForm,SignUpForm
from .models import User, Profile
from django.contrib.auth import login,authenticate,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        print(f"Phone number: {phone_number}, OTP: {otp}")
        if not phone_number or not otp:
            return JsonResponse({'error': 'Phone number and OTP are required'}, status=400)

        try:
            user = User.objects.get(phone_number=phone_number)

            # Verify OTP
            if user.verify_otp(otp):
                login(request,user)
                print("loginned")
                # token = user.generate_token()
                response = JsonResponse({'message': 'OTP verified successfully'})
                response.set_cookie(
                    key='sessionid',
                    value=request.session.session_key,
                    httponly=True,
                    secure=True,
                    samesite='None'
                 )
                return response
            else:
                return JsonResponse({'error': 'Invalid OTP'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method, use POST'}, status=405)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successfully'}, status=200)


    
@csrf_exempt
def signup(request):
    """Handle user sign up by sending OTP."""
    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        email = data.get('email')


        if not phone_number:
            return JsonResponse({'error': 'Phone number is required'}, status=400)

        # Check if the user already exists
        if User.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'error': 'User with this phone number already exists'}, status=400)

        user = User.objects.create(phone_number=phone_number,email=email)

        # Send OTP via Twilio
        otp = user.generate_otp()  
        user.save()

        # Send OTP SMS
        user.send_otp_sms()

        return JsonResponse({'message': 'OTP sent successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
@csrf_exempt

def loginn(request):
    """Handle user sign up by sending OTP."""
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("Request data:", data)  # Log the incoming request data
            
            phone_number = data.get('phone_number')
            
            if not phone_number:
                return JsonResponse({'error': 'Phone number is required'}, status=400)

            user = User.objects.filter(phone_number=phone_number).first()
           
            if not user:
                return JsonResponse({'error': 'User with this phone number does not exist'}, status=400)

            # Generate OTP
            otp = user.generate_otp()
           
            user.save()

            # Send OTP via SMS (Twilio or other service)
            user.send_otp_sms()
          

            return JsonResponse({'message': 'OTP sent successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)  # Catch all errors and log them
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt

def create_profile(request):
    if request.method == "POST":
        try:
            
           
            if request.content_type.startswith("multipart/form-data"):
                raw_post = request.POST
                user_data = {}
                for key in raw_post:
                    if key.startswith("userData["):
                        clean_key = key.replace("userData[", "").replace("]", "")
                        user_data[clean_key] = raw_post[key]
                       

            else:
                user_data = json.loads(request.body.decode("utf-8")).get("userData", {})

            print("Final userData parsed:", user_data)
             # Cleaning and validating data
            user_data = clean_data(user_data)
            image = request.FILES.get("userData[image]")  
            frontimage = request.FILES.get("userData[frontimage]")  
            backimage = request.FILES.get("userData[backimage]")  
            
           
            if not image or not frontimage or not backimage:
                return JsonResponse({"error": "All image files are required"}, status=400)
            phone_number = user_data.get("phone_number")
            if not phone_number:
                return JsonResponse({"error": "Phone number is required"}, status=400)

            user = User.objects.filter(phone_number=phone_number).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            if Profile.objects.filter(user=user).exists():
                return JsonResponse({"error": "Profile already exists"}, status=400)

            profile = Profile.objects.create(
                user=user,
                firstname=user_data.get("firstname"),
                middlename=user_data.get("middlename"),
                lastname=user_data.get("lastname") ,
                gender=user_data.get("gender"),
                dob=user_data.get("dob"),
                borndistrict=user_data.get("borndistrict"),
                bornward=user_data.get("bornward"),
                bornplace=user_data.get("bornplace"),
                currentdistrict=user_data.get("currentdistrict"),
                currentward=user_data.get("currentward"),
                currentplace=user_data.get("currentplace"),
                citizennumber=user_data.get("citizennumber"),
                issuedate=user_data.get("issuedate"),
                issueplace=user_data.get("issueplace"),
                father_firstname=user_data.get("father_firstname"),
                father_middlename=user_data.get("father_middlename"),
                father_lastname=user_data.get("father_lastname"),
                father_borndistrict=user_data.get("father_borndistrict"),
                father_bornward=user_data.get("father_bornward"),
                father_bornplace=user_data.get("father_bornplace"),
                mother_firstname=user_data.get("mother_firstname"),
                mother_middlename=user_data.get("mother_middlename"),
                mother_lastname=user_data.get("mother_lastname"),
                mother_borndistrict=user_data.get("mother_borndistrict"),
                mother_bornward=user_data.get("mother_bornward"),
                mother_bornplace=user_data.get("mother_bornplace"),
                partner_firstname=user_data.get("partner_firstname"),
                partner_middlename=user_data.get("partner_middlename"),
                partner_lastname=user_data.get("partner_lastname"),
                partner_borndistrict=user_data.get("partner_borndistrict"),
                partner_bornward=user_data.get("partner_bornward"),
                partner_bornplace=user_data.get("partner_bornplace"),
                image=image,
                frontimage=frontimage,
                backimage=backimage,
            )
            profile.save()
             # After creating the profile, log the user in
            user = User.objects.get(phone_number=user_data.get('phone_number'))
            login(request, user)  # This will create a session for the logged-in user
            return JsonResponse({"message": "Profile created successfully"}, status=201)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def clean_data(user_data):
    # Check and clean partner_bornward (and any other fields that require cleaning)
    if user_data.get("partner_bornward") == "null":
        user_data["partner_bornward"] = None
    else:
        try:
            user_data["partner_bornward"] = int(user_data.get("partner_bornward", ""))
        except (ValueError, TypeError):
            user_data["partner_bornward"] = None



    return user_data
@login_required
def check_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "user": request.user})
    return JsonResponse({"message": "Unauthorized"}, status=401)
        
@login_required

def view_profile(request):
    
    """View the logged-in user's profile."""
    if request.user.is_authenticated:

        user = request.user  # Get the currently logged-in user
        print(user)
        try:
            profile = user.profile  # Get the user's profile

            # Convert user and profile data to JSON serializable format
            user_data = {
                "id": user.id,
                "phone_number": user.phone_number,
                "email": user.email,
                "is_active": user.is_active,
            }

            profile_data = {
                "image": profile.image.url if profile.image else None,  # Convert ImageField to URL
                "frontimage": profile.frontimage.url if profile.frontimage else None,
                "backimage": profile.backimage.url if profile.backimage else None,
                "firstname": profile.firstname,
                "middlename": profile.middlename,
                "lastname": profile.lastname,
                "gender": profile.gender,
                "dob": profile.dob.strftime("%Y-%m-%d") if profile.dob else None,

                "borndistrict": profile.borndistrict,
                "bornward": profile.bornward,
                "bornplace": profile.bornplace,

                "currentdistrict": profile.currentdistrict,
                "currentward": profile.currentward,
                "currentplace": profile.currentplace,

                "citizennumber": profile.citizennumber,
                "issuedate": profile.issuedate.strftime("%Y-%m-%d") if profile.issuedate else None,
                "issueplace": profile.issueplace,

                "father_firstname": profile.father_firstname,
                "father_middlename": profile.father_middlename,
                "father_lastname": profile.father_lastname,
                "father_borndistrict": profile.father_borndistrict,
                "father_bornward": profile.father_bornward,
                "father_bornplace": profile.father_bornplace,

                "mother_firstname": profile.mother_firstname,
                "mother_middlename": profile.mother_middlename,
                "mother_lastname": profile.mother_lastname,
                "mother_borndistrict": profile.mother_borndistrict,
                "mother_bornward": profile.mother_bornward,
                "mother_bornplace": profile.mother_bornplace,

                "partner_firstname": profile.partner_firstname,
                "partner_middlename": profile.partner_middlename,
                "partner_lastname": profile.partner_lastname,
                "partner_borndistrict": profile.partner_borndistrict,
                "partner_bornward": profile.partner_bornward,
                "partner_bornplace": profile.partner_bornplace,
            }

            return JsonResponse({"user": user_data, "profile": profile_data})

        except Profile.DoesNotExist:
            return JsonResponse({"error": "Profile not found"}, status=404)
    return JsonResponse({"error": "User not authenticated"}, status=401)
