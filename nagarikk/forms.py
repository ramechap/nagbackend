from django import forms
from .models import Profile,User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "firstname", "middlename", "lastname", "gender", "dob",
            "borndistrict", "bornward", "bornplace",
            "currentdistrict", "currentward", "currentplace",
            "citizennumber", "issuedate", "issueplace",
            "image", "frontimage", "backimage",
            "father_firstname", "father_middlename", "father_lastname",
            "father_borndistrict", "father_bornward", "father_bornplace",
            "mother_firstname", "mother_middlename", "mother_lastname",
            "mother_borndistrict", "mother_bornward", "mother_bornplace",
            "partner_firstname", "partner_middlename", "partner_lastname",
            "partner_borndistrict", "partner_bornward", "partner_bornplace",
        ]

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["phone_number"]
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number is already registered.")
        return phone_number

class OTPVerificationForm(forms.Form):
    phone_number = forms.CharField()
    otp = forms.CharField(max_length=6)

    def clean_otp(self):
        otp = self.cleaned_data.get("otp")
        if not otp.isdigit():
            raise forms.ValidationError("OTP must be numeric.")
        return otp

class LoginWithOTPForm(forms.Form):
    phone_number = forms.CharField()
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number is not registered.")
        return phone_number