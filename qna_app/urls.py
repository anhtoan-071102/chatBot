from django.urls import path
from .views import AskView, ChatListView, ChatDetailView, RegisterView, LoginView

urlpatterns = [
    path('ask/', AskView.as_view(), name='ask'),
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/<int:chat_id>/', ChatDetailView.as_view(), name='chat-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]


# localhost/api/ask