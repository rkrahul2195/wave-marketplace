import string
import random
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest,HttpResponse
from sslcommerz_lib import SSLCOMMERZ

def unique_id(size=10,chars=string.ascii_uppercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    

def SSL_Payment(user_id,name,number,email,amount,address,id,item):
    settings = { 'store_id': 'wavem655a4206f322e', 
                'store_pass': 'wavem655a4206f322e@ssl', 
                'issandbox': True }
    sslcommez = SSLCOMMERZ(settings)
   
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = id
    
    post_body['success_url'] = "http://127.0.0.1:8000/payment/success"
    post_body['fail_url'] = "http://127.0.0.1:8000/"
    post_body['cancel_url'] = "http://127.0.0.1:8000/"
    post_body['emi_option'] = 0
    
    post_body['cus_name'] = name
    post_body['cus_email'] = email
    post_body['cus_phone'] = number
    post_body['cus_add1'] = address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = item
    post_body['product_category'] = "Digital Product"
    post_body['product_profile'] = "general"
    
    
    # Additional Information 
    post_body['value_a'] = amount
    post_body['value_b'] = item
    post_body['value_c'] = user_id
    post_body['value_d'] = id
    
    response = sslcommez.createSession(post_body)
    
    # print(response) 
    return 'https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"]