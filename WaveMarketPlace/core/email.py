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

def sent_notification(email,name,project_title):
    subject = "Congratulations! You've Been Awarded the Project"
    message = f"""Hello {name},
    Great news! You've won the project: {project_title} on our platform.\n 
    To get started, confirm your acceptance by clicking "Accept" 
    on the project page. Reach out to the client for any clarifications, 
    and ensure you meet the project's deadline.
    Your success is our success!\n\n\n
    Best wishes,
    """
    send_mail(subject, message, 'admin@wave.com.bd', [email])

