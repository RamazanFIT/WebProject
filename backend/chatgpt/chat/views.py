from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import ChatgptHistory, ChatGroup
from .serializers import (ChatgptHistorySerializer, ChatGptSerializer, ChatGroupSerializer, FullChatGroupSerializer)
from django.shortcuts import get_object_or_404
from users.models import User
# swagger 
from drf_yasg.utils import swagger_auto_schema

# permissions 
from users.views import isAuthenticated, checkAuthentication

# chatgpt 
from chat.chatgpt import generate_response
from .prompt import prompt

class ChatGptViewSet(viewsets.ModelViewSet):
    queryset = ChatgptHistory.objects.all()
    serializer_class = ChatgptHistorySerializer
    
    @swagger_auto_schema(operation_summary="chatgpt", request_body=ChatGptSerializer)
    def get_chatgpt_response(cls, request, id):
        if not isAuthenticated(request): return Response(data={"detail" : "Plz do Authentications"})
        chat = ChatGroup.objects.get(pk=id)
        user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
        if chat.user != user:  return Response(data={"detail" : "permission denied"})
        serializer = ChatGptSerializer(data=request.data)
        if serializer.is_valid():
            chatgpt_message = generate_response(prompt + cls.get_history_in_str(request, id) + "(( " + serializer.data.get("message") + " ))")
            # saving data 
            user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
            group = ChatGroup.objects.get(pk=id)
            data = ChatgptHistory(response_message=chatgpt_message, message=serializer.data.get("message"), user_id=user, chat_group=group)
            data.save()
            return Response(data=chatgpt_message)
        else:
            return Response(data={"detail" : serializer.errors})
        
    @swagger_auto_schema(operation_summary="All history of messages with ChatGpt")
    def get_history(cls, request, id):
        if not isAuthenticated(request): return Response(data={"detail" : "Plz do Authentications"})
        try:
            group = ChatGroup.objects.get(pk=id)
            user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
            if group.user != user:  return Response(data={"detail" : "permission denied"})
            messages = ChatgptHistory.objects.filter(user_id=checkAuthentication(request).data.get('id'), chat_group=group).order_by('-created_at')
            serilaizer = ChatgptHistorySerializer(instance=messages, many=True)
            return Response(serilaizer.data)
        except:
            return Response(data={"detail" : "some error"}, status=status.HTTP_404_NOT_FOUND)
            
    def get_history_in_str(cls, request, id : int):
        if not isAuthenticated(request): return Response(data={"detail" : "Plz do Authentications"})
        try:
            user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
            avg_word = 5
            max_token = 20 * avg_word
            str_response = ""
            stop = False
            check_list = cls.get_history(request, id).data
            # print(check_list) 
            for ii in range(len(check_list)):
                i = check_list[ii]
                if stop: break
                if 'detail' in i.keys():
                    return Response(data={"detail" : "some error"}, status=status.HTTP_404_NOT_FOUND)
                for j in i['message']:
                    if stop: break
                    if len(str_response) >= max_token: stop = True
                    str_response += j 
                for j in i['response_message']:
                    if stop: break
                    if len(str_response) >= max_token: stop = True
                    str_response += j 
            
            return str_response
        except:
            return "" 
        
    @swagger_auto_schema(operation_summary="creating the new chat with chatgpt", request_body=ChatGroupSerializer)
    def create_new_chat(cls, request):
        if not isAuthenticated(request):
            return Response(data={"detail" : "permission denied"})
        try:
            user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
            # label = "Chat with your future"
            label = request.data['label']
            new_chat = ChatGroup.objects.create(user=user, label=label)
            serializer = FullChatGroupSerializer(instance=new_chat)
            return Response(data=serializer.data)
        except:
            return Response(data={"detail" : "some error"}, status=status.HTTP_404_NOT_FOUND)
        
    def get_all_chats(cls, request):
        if not isAuthenticated(request):
            return Response(data={"detail" : "permission denied"})
        user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
        chats = ChatGroup.objects.filter(user=user)
        serializer = FullChatGroupSerializer(instance=chats, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_summary="changing and posting the new label to chat", request_body=ChatGroupSerializer)
    def change_label(cls, request, id):
        if not isAuthenticated(request):
            return Response(data={"detail" : "permission denied"})
        chat = ChatGroup.objects.get(pk=id)
        user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
        if chat.user != user:  return Response(data={"detail" : "permission denied"})
        chat.label = request.data['label']
        chat.save()
        serializer = FullChatGroupSerializer(instance=chat)
        return Response(data=serializer.data)
    
    def delete_chat(cls, request, id : int):
        if not isAuthenticated(request):
            return Response(data={"detail" : "permission denied"})
        user = User.objects.get(pk=checkAuthentication(request).data.get('id'))
        chat = ChatGroup.objects.get(pk=id)
        if chat.user != user:  return Response(data={"detail" : "permission denied"})
        chat.delete()
        return Response(data={'detail' : 'success'})
    
    