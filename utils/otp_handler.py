from django.utils.crypto import get_random_string
from .functions import isValidEmail, sendEmailOTP
from logs.models import OTPLog
import requests

# TODO DONE
# ** OTP HANDLER CLASS 
class OTPHandler:
    
    @staticmethod
    def generate_otp(email):
        # Generate 6-digit OTP
        otp = get_random_string(length=6, allowed_chars='1234567890')
        if not isValidEmail(email):
            raise ValueError("Invalid Email")
        sendEmailOTP(email, otp, "registration")
        return {'OTP': otp}

    @staticmethod
    def verifyOTP(email, otp): 
        db_otp = OTPLog.objects.filter(email=email, purpose="registration", otp=otp, status='generated').first()
        print(db_otp, otp)
        if not db_otp:   
            raise ValueError("Invalid OTP")
        else:         
            OTPLog.objects.filter(email=email, purpose="registration", otp=otp, status='generated').update(status='verified')
            return True 


