import re
from logs.models import OTPLog
from django.core.mail import send_mail
import environ
env = environ.Env()

# TODO DONE
def isValidEmail(email):
    if(email == None):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return True if re.search(pattern, email) else False

# TODO DONE
def sendEmailOTP(email, otp, purpose):
    try:
        subject = 'OTP Verification From IT Services'
        content = f"Here is Your OTP: {otp}"
        send_mail(
            subject, 
            content, 
            env('ENV_EMAIL_HOST_USER'),
            [email],    
        )         
        print("send email otp::::::::", email, otp, purpose)       
        otp_log = OTPLog.objects.create(otp=otp, email=email, purpose=purpose, content=content)
        otp_log.save()
        return "OTP email sent successfully."
    except Exception as e:
        raise e

