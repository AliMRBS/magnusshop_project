import requests
from django.conf import settings

def apardakht_request_handler(amount, mobile, email, description, callback_url):
    url = settings.AGHAYEPARDAKHT['gateway_create_url']
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "pin": "sandbox",  
        "amount": float(amount),
        "mobile": mobile,
        "email": email,
        "description": description,
        "callback":settings.AGHAYEPARDAKHT['gateway_callback_url'],  
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    
    if response.status_code == 200 and result.get("status") == "success":
        transid = result["transid"] 
        payment_url = f"https://panel.aqayepardakht.ir/startpay/sandbox/{transid}"
        return payment_url, transid
    else:
        return None, None


def apardakht_payment_checker(amount, transid):
    url = settings.AGHAYEPARDAKHT['gateway_verify_url']
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "pin": "sandbox",  
        "amount": amount,
        "transid": transid,  
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    if response.status_code == 200 and result.get("code") == "1":
        is_paid = True
        payment_details = {
            "cardnumber": result.get("cardnumber"),
            "tracking_number": result.get("tracking_number"),
            "bank": result.get("bank"),
            "invoice_id": result.get("invoice_id"),
        }
        return is_paid, payment_details
    else:
        return False, None
