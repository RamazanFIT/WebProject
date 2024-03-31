from rest_framework.response import Response
from users.models import *
from users.serializers import (

                            SendToEmailSerializer,

)
from django.shortcuts import get_object_or_404
import jwt, datetime
from django.core.mail import send_mail
from django.conf import settings






def send_the_email(request, message, subject, email):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Сброс пароля</title>
<style>
  body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    padding: 20px;
  }
  .container {
    max-width: 600px;
    margin: 0 auto;
    background-color: #fff;
    border-radius: 5px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  h1 {
    text-align: center;
    color: #333;
  }
  p {
    margin-bottom: 20px;
    color: #555;
  }
  .code {
    font-size: 24px;
    text-align: center;
    color: #007bff;
    margin-bottom: 30px;
  }
  .footer {
    text-align: center;
    margin-top: 20px;
    color: #888;
  }
</style>
</head>
<body>
  <div class="container">
    <h1>Сброс пароля</h1>
    <p>Вы запросили сброс пароля для вашей учетной записи. Ниже приведен ваш код для сброса пароля:</p>
    <div class="code">""" + f"""{message}""" + """</div>
    <p>Если вы не запрашивали сброс пароля, проигнорируйте это сообщение.</p>
    <p class="footer">С уважением,<br>Rent4</p>
  </div>
</body>
</html>
"""
    serilizer = SendToEmailSerializer(data=request.data)
    if serilizer.is_valid():
        from_email = settings.EMAIL_HOST_USER
        fail_silently = False
        recipient_list = email
        send_mail(
            subject,
            message, 
            from_email,
            [recipient_list],  
            fail_silently=fail_silently,
            html_message=html_content
        )
        return (True, Response(data={'status' : 'success'}))
    else:
        return (False, Response(data=serilizer.errors))

