import random 
from django.core.mail import send_mail
from django.utils.crypto import get_random_string 

def sent_email_verification(email,name):
    print(f'Registration Name : {name} Email :{email}')

    verification_code = random.randint(100000, 999999)
    subject = 'Account Verification Code'
    message = f"""Hello {name},
    Thank you for signing up with Wave!\n
    Your verification code is: {verification_code}

    Best regards,
    The Wave Team
    Bangladeshi Freelancer Marketplace
    """
    send_mail(subject, message, 'rkrahul.diu.672@gmail.com', [email])
    return  verification_code