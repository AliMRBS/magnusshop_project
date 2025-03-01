from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = "کد تایید ایمیل شما در مگنوس شاپ"  
    message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px; background-color: #f4f4f4;">
        <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #333;">فروشگاه مگنوس شاپ</h2>
            <p style="font-size: 30px; color: #555;">کد تأیید شما:</p>
            <p style="font-size: 50px; font-weight: bold; color: #007bff; margin: 10px 0;">{otp}</p>
            <p style="font-size: 28px; color: #777;">این کد فقط <strong>۲ دقیقه</strong> معتبر است.</p>
            <p style="font-size: 24px; color: #777;">https://magnusshop.ir</p>
        </div>
    </body>
    </html>
    """
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [email], html_message=message)

