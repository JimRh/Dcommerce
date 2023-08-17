
from sslcommerz_lib import SSLCOMMERZ     
def make_payment(total_price,tran_id,username,userid,shipping_address,contact_number):
    settings = { 'store_id': 'dcomm64dd351e0f742', 'store_pass': 'dcomm64dd351e0f742@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = int(total_price)
    post_body['currency'] = "BDT"
    post_body['tran_id'] = tran_id
    post_body['success_url'] = f'https://localhost:8000/auth/paymentsuccess/{userid}/{shipping_address}/{contact_number}'
    post_body['fail_url'] = "your fail url"
    post_body['cancel_url'] = "your cancel url"
    post_body['emi_option'] = 0
    post_body['cus_name'] = username
    post_body['cus_email'] = "test@test.com"
    post_body['cus_phone'] = contact_number
    post_body['cus_add1'] = shipping_address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"
   



    response = sslcz.createSession(post_body) # API response
    return response