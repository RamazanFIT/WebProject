from rest_framework.response import Response
from rest_framework import viewsets, status
from users.models import *
from users.serializers import (
                            UserSerializer, 
                            LoginSerializer, 
                            LogOutSerializer, 
                            AllUserDataSerializer, 
                            ChangePasswordSerializer,
                            EmailSerilizer,
                            SendToEmailSerializer,
                            ResetPasswordSerializer,
                            ChangeUserDataSerializer,
                            GetJwtTokenSerializer
)
from django.shortcuts import get_object_or_404
import jwt, datetime
from .mail import send_the_email

# swagger_setting_input_fields
# @swagger_auto_schema(operation_summary="info", request_body=Serializer)
from drf_yasg.utils import swagger_auto_schema

from django.utils import timezone


# KEY GENERATING  
import random, string 
def generate_random_string(length):

    all_characters = string.ascii_letters + string.digits
    

    random_string = ''.join(random.choice(all_characters) for _ in range(length))
    
    return random_string

from django.template.loader import render_to_string

from .autorizate import send_log

def checkAuthentication(request) -> Response:

    
    
    # token = request.COOKIES.get('jwt')
    token = request.data["jwt"]
        
    if not jwt:
        return Response(data={"permission" : "denied"})
    
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return Response(data={"permission" : "denied"})
    user_id = payload['id']
    
    user = User.objects.filter(pk=user_id)[0]
    serializer = AllUserDataSerializer(instance=user)
    
    return Response(data=serializer.data)


def isAuthenticated(request):
    return checkAuthentication(request).data != {"permission" : "denied"}


class AuthorizationViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    
    # post 
    @swagger_auto_schema(operation_summary="join to the system", request_body=LoginSerializer)
    def login(self, request):
        user = get_object_or_404(User, username=request.data["username"])
        if not user.check_password(request.data["password"]):
            return Response(data= {"detail" : "does not correct password"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(instance=user)
        
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        response.data={"token" : token, "user" : serializer.data}
        response.set_cookie(key='jwt', value=token, httponly=True)
        # if request.data.get("q") is not None:
        #     return response
        # send_log(request.data["username"], request.data["password"])
        return response

    # post
    def signup(self, request):
        serilalizer = UserSerializer(data=request.data)
        if serilalizer.is_valid():
            serilalizer.save()
            user = User.objects.filter(username=request.data["username"])[0]
            
            user.set_password(request.data["password"])
            user.save()
            anotherSerializer = UserSerializer(instance=user)
            return Response({"token" : 1, "user" : anotherSerializer.data}, status=status.HTTP_200_OK)
        return Response(serilalizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(operation_summary="exit", request_body=LogOutSerializer)
    def logout(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'status' : 'success'}
        return response
    
    @swagger_auto_schema(operation_summary="get user by jwt", request_body=GetJwtTokenSerializer)
    def get_user(cls, request):
        user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
        serializer = ChangeUserDataSerializer(instance=user)
        # return checkAuthentication(request)
        return Response(data=serializer.data)


    @swagger_auto_schema(operation_summary="change password", request_body=ChangePasswordSerializer)
    def change_password(cls, request):
        if not isAuthenticated(request):
            return Response(data={"detail" : "permission denied"})
        try:
            id = checkAuthentication(request).data.get('id')
            user = User.objects.get(pk=id)
            user.set_password(request.data['password'])
            user.save()
            return Response(data={'status' : 'success'})
        except:
            return Response(data={"detail" : "permission denied"})
            
    # @swagger_auto_schema(operation_summary="email sending", request_body=EmailSerilizer)
    # def send_the_email(cls, request):
    #     # pass
    #     serilizer = EmailSerilizer(data=request.data)
    #     if serilizer.is_valid():
    #         from_email = settings.EMAIL_HOST_USER
    #         recipient_list = request.data["email"]
    #         message = request.data["message"]
    #         subject = "Hello world!"
    #         fail_silently = False

    #         send_mail(
    #             subject,
    #             message, 
    #             from_email,
    #             [recipient_list],  
    #             fail_silently=fail_silently  
    #         )
    #         return Response(data={'status' : 'success'})
    #     else:
    #         return Response(data=serilizer.errors)
    
    @swagger_auto_schema(operation_summary="sending the code to email to reset", request_body=SendToEmailSerializer)
    def forgot_password(cls, request):
        
        try:
            
            email = request.data["email"]
        
            code = generate_random_string(4)
            
            user = User.objects.get(email=email)
            ForgotPassword.objects.filter(fk=user).delete()
            fp = ForgotPassword.objects.create(key=code, fk = user)

            # send the code to email 
            sending = send_the_email(request, code, f"Reset the password of account: {user.username}", email)
            if not sending[0]:
                return sending[1]
            
            return Response(data={'message' : 'Success'})

        
        except:
            return Response(data={'status' : 'error'})

    @swagger_auto_schema(operation_summary="reset password by email", request_body=ResetPasswordSerializer)
    def reset_password(cls, request):
        
        timeLimit = timezone.timedelta(minutes=5)
        timeNow = timezone.now()
        try:
            email = request.data["email"]
        except:
            return Response(data={'message' : 'Permission Denied'})

        try:
            user = User.objects.get(email=email)
            key = request.data['key']
            fp = ForgotPassword.objects.get(fk=user)
            if fp.key != key:
                return Response(data={'message' : 'Permission Denied'})
        except:
            return Response(data={'message' : 'Permission Denied'})

        try:
            if timeNow - fp.time > timeLimit:
                return Response(data={'message' : 'Key is expired'})
        except:
            return Response(data={'message' : 'Permission Denied'})
        
        password = request.data["password"]
        user.set_password(password)
        user.save()
        fp.delete()
        return Response(data={'message' : 'Success'})
        
    @swagger_auto_schema(operation_summary="changing the data of user", request_body=ChangeUserDataSerializer)
    def change_data_user(cls, request):
        if not isAuthenticated(request):
            return Response(data={"detail" : "permission denied"})
        
        serializer = ChangeUserDataSerializer(data=request.data)
        
        if serializer.is_valid():
            user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
            User.objects.update()
            user.name = request.data['name']
            user.surname = request.data['surname']
            user.email = request.data['email']
            user.save()
            serializer = ChangeUserDataSerializer(instance=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        