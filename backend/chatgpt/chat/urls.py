from rest_framework import routers
from django.urls import include, path
from .views import ChatGptViewSet

app_name = 'chatgpt'


urlpatterns = [

    path('message/<int:id>/', ChatGptViewSet.as_view({'post': 'get_chatgpt_response'}), name="get_chatgpt_response"),
    path('history/<int:id>/', ChatGptViewSet.as_view({'get': 'get_history'}), name="get_history"),
    path('start/', ChatGptViewSet.as_view({'post': 'create_new_chat'}), name="create_new_chat"),
    path('chats/', ChatGptViewSet.as_view({'get': 'get_all_chats'}), name="get_all_chats"),
    path('chats/change/<int:id>', ChatGptViewSet.as_view({'put': 'change_label'}), name="change_label"),
    path('chats/delete/<int:id>', ChatGptViewSet.as_view({'delete': 'delete_chat'}), name="delete_chat"),

]

